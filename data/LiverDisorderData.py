from ucimlrepo import fetch_ucirepo 

import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def get_liver_dataloaders(batch_size=32):
    # fetch dataset 
    liver_disorders = fetch_ucirepo(id=60) 
    
    # data (as pandas dataframes) 
    X = liver_disorders.data.features 
    y = liver_disorders.data.targets 

    #Convert to numpy first
    X = X.to_numpy().astype(np.float32)
    y = y.to_numpy().astype(np.float32)

    if len(y.shape) == 1:
        y = y.reshape(-1, 1)

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
    loader_train = DataLoader(dataset_train, batch_size=32, shuffle=True)

    dataset_test = TensorDataset(X_test, y_test)
    loader_test = DataLoader(dataset_test, batch_size=32, shuffle=True)

    return loader_train, loader_test