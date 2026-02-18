#pip install ucimlrepo
from ucimlrepo import fetch_ucirepo 

import numpy as np

import torch
import torch.nn as nn 
import torch.nn.functional as F 

from torch.optim import Adam
from torch.utils.data import TensorDataset, DataLoader

import lightning as L
  
# fetch dataset 
liver_disorders = fetch_ucirepo(id=60) 
  
# data (as pandas dataframes) 
X = liver_disorders.data.features 
y = liver_disorders.data.targets 

# Convert to numpy
X = X.to_numpy().astype(np.float32)
y = y.to_numpy().astype(np.float32)

# If y is shape (n,1) keep it that way
if len(y.shape) == 1:
    y = y.reshape(-1, 1)

# Convert to torch tensors
X_tensor = torch.tensor(X)
y_tensor = torch.tensor(y)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=32, shuffle=True)
  
# metadata 
print(liver_disorders.metadata) 
  
# variable information 
print(liver_disorders.variables) 

class LiverDisorderModel(nn.Module):
    def __init__(self, input_size):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()  # Binary classification
        )

    def forward(self, input):
        return self.model(input)
