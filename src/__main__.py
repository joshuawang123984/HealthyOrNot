import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd

from data.ToDataloader_numeric import ucirepo_to_df, csv_to_df, df_to_xy
from models.LinearRegression import LinearRegression
from models.LogisticRegression import LogisticReg
from models.RandomForest import random_forest_regressor_model, random_forest_classifier_model
from models.SmallMLPClassification import SmallMLPClassification
from models.SmallMLPRegression import SmallMLPRegression
from models.SVModels import SVR_model, SVC_model
from models.TreeModels import decision_tree_classifier, decision_tree_regressor
from models.KNN import KNN

import json

def process_dataset(dataset, X, y):
    if dataset["task"].lower() == "classification":
        best_name, best_model = run_classification(X, y)
    else:
        best_name, best_model = run_regression(X, y)

    print(f"Best model for {dataset['name']}: {best_name}")
    predictions = best_model.predict(X)
    print(predictions[0])
    print(predictions[19])
    print(predictions[20])

def main():
    with open("./data/csv_data.json", "r") as f:
        csv_data = json.load(f)

    for dataset in csv_data:
        df = csv_to_df(dataset["path"])
        if dataset.get("sample"):
            df = df.sample(n=dataset["sample"], random_state=42)
        X, y = df_to_xy(df, target_col=dataset["target_col"])
        process_dataset(dataset, X, y)
        

    with open("./data/ucirepo_data.json", "r") as f:
        ucirepo_data = json.load(f)

    for dataset in ucirepo_data:
        X, y = ucirepo_to_df(dataset["id"])
        X = X.dropna()
        y = y.loc[X.index]

        if "mappings" in dataset:
            for col, mapping in dataset["mappings"].items():
                X[col] = X[col].map(mapping)
        
        if "target_mapping" in dataset:
            y = y.squeeze().map(dataset["target_mapping"]).to_numpy().astype(np.float32)
        else:
            y = y.to_numpy().astype(np.float32).squeeze()

       
        print(f"{dataset['name']}: X shape={X.shape}, y shape={y.shape}")
        process_dataset(dataset, X, y)

def cross_validate(X, y, model_fn, k):
    X = np.array_split(X, k)
    y = np.array_split(y, k)
    scores = []

    for i in range(k):
        X_test = X[i]
        y_test = y[i]

        X_train = np.concatenate([X[j] for j in range(k) if j != i])
        y_train = np.concatenate([y[j] for j in range(k) if j != i])

        target_model = model_fn(X_train, y_train)
        score = target_model.score(X_test, y_test)

        scores.append(score)
    
    score_mean = sum(scores) / k
    score_std = np.std(scores)

    return score_mean, score_std
        

def run_classification(X, y):
    models = {
        "knn": lambda X, y: KNN(X, y),
        "logistic": lambda X, y: LogisticReg(X, y),
        "decision_tree": lambda X, y: decision_tree_classifier(X, y),
        "random_forest": lambda X, y: random_forest_classifier_model(X, y),
        "svc": lambda X, y: SVC_model(X, y),
    }

    best_name, best_score = None, -float('inf')
    for name, model_fn in models.items():
        score_mean, score_std = cross_validate(X, y, model_fn, k=5)

        print(f"{name}: {score_mean:.4f} +- {score_std:.4f}")

        if score_mean > best_score:
            best_score = score_mean
            best_name = name

    print(f"\nBest: {best_name} ({best_score:.4f})")
    best_model = models[best_name](X,y)
    return best_name, best_model

def run_regression(X, y):
    models = {
        "linear": lambda X, y: LinearRegression(X, y),
        #have to experiment with multiple alpha vals, create a lsit and go thru each maybe, but make diff exp eg: 0.001, 0.01, 0.1
        "ridge": lambda X, y: LinearRegression(X, y, 0.01, ridge=True),
        "lasso": lambda X, y: LinearRegression(X, y, 0.01, lasso=True),
        "decision_tree": lambda X, y:  decision_tree_regressor(X, y),
        "random_forest": lambda X, y: random_forest_regressor_model(X, y),
        "svr": lambda X, y: SVR_model(X, y),
    }

    best_name, best_score = None, -float('inf')
    for name, model_fn in models.items():
        score_mean, score_std = cross_validate(X, y, model_fn, k=5)

        print(f"{name}: {score_mean:.4f} +- {score_std:.4f}")
        
        if score_mean > best_score:
            best_score = score_mean
            best_name = name

    print(f"\nBest: {best_name} ({best_score:.4f})")
    best_model = models[best_name](X,y)
    return best_name, best_model

if __name__ == '__main__':
    main()