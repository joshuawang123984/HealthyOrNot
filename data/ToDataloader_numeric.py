from ucimlrepo import fetch_ucirepo 

import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import kagglehub
import pandas as pd

from pathlib import Path

def ucirepo_to_df(id):
    dataset = fetch_ucirepo(id=id) 

    #data (as pandas dataframes) 
    X = dataset.data.features 
    y = dataset.data.targets 

    return X, y

def csv_to_df(filepath, index_col=None):
    df = pd.read_csv(filepath, index_col=index_col)

    return df

def kaggle_download_to_df(path, filename=None):
    download_path = kagglehub.dataset_download(path)
    csv_files = list(Path(download_path).glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {download_path}")
    
    if filename:
        match = [f for f in csv_files if f.name == filename]
        if not match:
            raise FileNotFoundError(f"{filename} not found. Available: {[f.name for f in csv_files]}")
        return pd.read_csv(match[0])
    
    return pd.read_csv(csv_files[0])

def df_to_xy(df, target_col):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y

#transforms to float32, so categorical may not work
def xy_to_dataloader(X, y, batch_size=32):

    #Convert to numpy first
    X = X.to_numpy().astype(np.float32)
    y = y.to_numpy().astype(np.float32)

    #Split FIRST
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    #Fit scaler ONLY on training data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    #Convert to tensors
    X_train = torch.tensor(X_train)
    X_test = torch.tensor(X_test)
    y_train = torch.tensor(y_train)
    y_test = torch.tensor(y_test)


    dataset_train = TensorDataset(X_train, y_train)
    loader_train = DataLoader(dataset_train, batch_size=batch_size, shuffle=True)

    dataset_test = TensorDataset(X_test, y_test)
    loader_test = DataLoader(dataset_test, batch_size=batch_size, shuffle=False)

    return loader_train, loader_test, scaler