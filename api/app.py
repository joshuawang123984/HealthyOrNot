from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.__main__ import run_classification, run_regression
from data.ToDataloader_numeric import csv_to_df, df_to_xy

import json
import joblib

trained_models = {}
dataset_metadata = {}

def load_models():
    save_dir = os.path.join(BASE_DIR, 'saved_models')
    os.makedirs(save_dir, exist_ok=True)

    with open(os.path.join(BASE_DIR, 'data', 'csv_data.json'), 'r') as f:
        csv_data = json.load(f)

    with open(os.path.join(BASE_DIR, 'data', 'csv_descriptions.json'), 'r') as f:
        descriptions = json.load(f)

    for dataset in csv_data:
        save_path = os.path.join(save_dir, f"{dataset['name']}_model.pkl")
        print(f"Save path: {save_path}")
        print(f"Exists: {os.path.exists(save_path)}")
        
        df = csv_to_df(dataset['path'])
        df = df.sample(n=500, random_state=42)
        X, y = df_to_xy(df, target_col=dataset['target_col'])

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
            **descriptions.get(dataset['name'], {})
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
    
    return jsonify({'prediction': int(prediction[0])})

@app.route('/datasets', methods=['GET'])
def datasets():
    return jsonify(dataset_metadata)

if __name__ == '__main__':
    load_models()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))