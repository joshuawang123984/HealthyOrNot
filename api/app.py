from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.__main__ import run_classification, run_regression
from data.ToDataloader_numeric import csv_to_df, df_to_xy, ucirepo_to_df

import json
import joblib

trained_models = {}
dataset_metadata = {}

#can also impute with median and mean of column vals then remove this dataset from skip set.
skip = {"chronic_kidney_disease"}

def load_models(data_file, descriptions_file):
    save_dir = os.path.join(BASE_DIR, 'saved_models')
    os.makedirs(save_dir, exist_ok=True)

    with open(os.path.join(BASE_DIR, 'data', data_file), 'r') as f:
        csv_data = json.load(f)

    with open(os.path.join(BASE_DIR, 'data', descriptions_file), 'r') as f:
        descriptions = json.load(f)

    for dataset in csv_data:
        if dataset['name'] in skip:
            continue

        save_path = os.path.join(save_dir, f"{dataset['name']}_model.pkl")
        print(f"Save path: {save_path}")
        print(f"Exists: {os.path.exists(save_path)}")
        
        if 'path' in dataset:
            df = csv_to_df(dataset['path'])
            df = df.sample(n=min(500, len(df)), random_state=42)
            X, y = df_to_xy(df, target_col=dataset['target_col'])
            y = y.values.ravel() 
        elif 'id' in dataset:
            X, y = ucirepo_to_df(dataset['id'])
    
            # Convert categorical columns to numeric
            X = X.apply(lambda col: pd.factorize(col)[0] if col.dtype == 'object' else col)
            
            mask = X.notna().all(axis=1)
            X = X[mask]
            y = y[mask]

            X = X.sample(n=min(500, len(X)), random_state=42)
            y = y.loc[X.index]
            y = y.values.ravel()

        else:
            print(f"Skipping {dataset['name']}: no data source found")
            continue

        if os.path.exists(save_path):
            best_model = joblib.load(save_path)
        else:
            if dataset['task'].lower() == 'classification':
                best_name, best_model = run_classification(X, y)
            else:
                best_name, best_model = run_regression(X, y)

            joblib.dump(best_model, save_path)

        trained_models[dataset['name']] = best_model
        dataset_metadata[dataset['name']] = {
            'features': list(X.columns),
            'task': dataset['task'],
            'target_map': dataset["target_map"],
            'target_desc': dataset["target_desc"],
            'features_desc': descriptions.get(dataset['name'], {}).get('features_desc', {})
        }

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://healthyornot.vercel.app"
])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    dataset_name = data['dataset']
    features = data['features']  # list of values from the frontend
    
    model = trained_models[dataset_name]
    feature_names = dataset_metadata[dataset_name]['features']
    
    X = pd.DataFrame([features], columns=feature_names)
    prediction = model.predict(X)
    
    print(type(prediction))
    if hasattr(prediction, "__len__"):
        #if the nparray is 1 dimensional, access the element
        try:
            return jsonify({'prediction': int(prediction[0])})
        #if the nparray is 0 dimensional:
        except:
            return jsonify({'prediction': int(prediction)})
    
    return jsonify({'prediction': int(prediction)})

@app.route('/datasets', methods=['GET'])
def datasets():
    return jsonify(dataset_metadata)

if __name__ == '__main__':
    all_data = ["csv_data.json", "ucirepo_data.json"]
    all_descriptions = ["csv_descriptions.json", "ucirepo_descriptions.json"]

    for (data, description) in zip(all_data, all_descriptions):
        load_models(data, description)
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))