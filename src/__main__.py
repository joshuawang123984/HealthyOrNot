from data.ToDataloader_numeric import ucirepo_to_df, csv_to_df, xy_to_dataloader
from models.FeatureSelectionRegressionModels import ridge_model, lasso_model
from models.LinearRegression import LinearRegression
from models.LogisticRegression import LogisticReg
from models.RandomForest import random_forest_regressor_model, random_forest_classifier_model
from models.SmallMLPClassification import SmallMLPClassification
from models.SmallMLPRegression import SmallMLPRegression
from models.SVModels import SVR_model, SVC_model
from models.TreeModels import decision_tree_classifier, decision_tree_regressor
from models.KNN import knn_classifier

from data.ToDataloader_numeric import ucirepo_to_df, csv_to_df, kaggle_download_to_df, df_to_xy

import json
from sklearn.model_selection import train_test_split


def main():
    with open("./src/data/csv_data.json", "r") as f:
        csv_data = json.load(f)

    for dataset in csv_data:
        df = csv_to_df(dataset["path"])
        X, y = df_to_xy(df, target_col=dataset["target_col"])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if dataset["task"] == "classification":
            best_model = run_classification(X_train, X_test, y_train, y_test)
        elif dataset["task"] == "regression":
            best_model = run_regression(X_train, X_test, y_train, y_test)

        print(f"Best model for {dataset['name']}: {best_model}")
    #have diff func for each model and dataload. then combine at the end in main

def run_classification(X_train, X_test, y_train, y_test):
    models = {
        "knn": knn_classifier(X_train, y_train),
        "logistic": LogisticReg(X_train, y_train),
        "decision_tree": decision_tree_classifier(X_train, y_train),
        "random_forest": random_forest_classifier_model(X_train, y_train),
        "svc": SVC_model(X_train, y_train),
    }

    best_name, best_model, best_score = None, None, -1
    for name, model in models.items():
        score = model.score(X_test, y_test)
        print(f"{name}: {score:.4f}")
        if score > best_score:
            best_score = score
            best_name = name
            best_model = model

    print(f"\nBest: {best_name} ({best_score:.4f})")
    return best_model

def run_regression(X_train, X_test, y_train, y_test):
    models = {
        "linear": LinearRegression(X_train, y_train),
        "ridge": ridge_model(X_train, y_train),
        "lasso": lasso_model(X_train, y_train),
        "decision_tree": decision_tree_regressor(X_train, y_train),
        "random_forest": random_forest_regressor_model(X_train, y_train),
        "svr": SVR_model(X_train, y_train),
    }

    best_name, best_model, best_score = None, None, -1
    for name, model in models.items():
        score = model.score(X_test, y_test)
        print(f"{name}: {score:.4f}")
        if score > best_score:
            best_score = score
            best_name = name
            best_model = model

    print(f"\nBest: {best_name} ({best_score:.4f})")
    return best_model

if __name__ == '__main__':
    main()