from data.ToDataloader_numeric import ucirepo_to_df, csv_to_df, xy_to_dataloader



from models.FeatureSelectionRegressionModels import ridge_model, lasso_model
from models.LinearRegression import LinearRegression
from models.LogisticRegression import LogisticReg
from models.RandomForestRegressor import random_forest_regressor_model
from models.SmallMLPClassification import SmallMLPClassification
from models.SmallMLPRegression import SmallMLPRegression
from models.SVRModel import SVR_model
from models.TreeModels import random_tree_model, decision_tree_model

import json


def main():
    with open("./src/data/csv_data.json", "r") as f:
        csv_data = json.load(f)

    for dataset in csv_data:
        print(dataset["name"], dataset["path"])
    #have diff func for each model and dataload. then combine at the end in main

if __name__ == '__main__':
    main()