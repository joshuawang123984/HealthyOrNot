import torch
import torch.nn as nn

class LogisticRegModel(nn.Module):
    def __init__(self, input_dim, num_classes):
        super().__init__()
        self.linear = nn.Linear(input_dim, num_classes)
    
    def forward(self, x):
        return self.linear(x)

class LogisticReg:
    def __init__(self, X_train, y_train, epochs=1000, lr=0.01):
        input_dim = X_train.shape[1]
        num_classes = len(y_train.unique() if hasattr(y_train, 'unique') else torch.unique(torch.tensor(y_train)))
        self.model = LogisticRegModel(input_dim, num_classes)
        self.fit(X_train, y_train, epochs, lr)

    def fit(self, X_train, y_train, epochs, lr):
        X = torch.tensor(X_train.values if hasattr(X_train, 'values') else X_train, dtype=torch.float32)
        y = torch.tensor(y_train.values if hasattr(y_train, 'values') else y_train, dtype=torch.long).squeeze()

        self.X_mean = X.mean(0)
        self.X_std = X.std(0) + 1e-8
        X = (X - self.X_mean) / self.X_std

        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        loss_fn = nn.CrossEntropyLoss()

        for _ in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            loss = loss_fn(self.model(X), y)
            loss.backward()
            optimizer.step()

    def score(self, X_test, y_test):
        X = torch.tensor(X_test.values if hasattr(X_test, 'values') else X_test, dtype=torch.float32)
        y = torch.tensor(y_test.values if hasattr(y_test, 'values') else y_test, dtype=torch.long).squeeze()

        X = (X - self.X_mean) / self.X_std

        self.model.eval()
        with torch.no_grad():
            preds = self.model(X)
            predicted_classes = torch.argmax(preds, dim=1)
        
        accuracy = (predicted_classes == y).float().mean().item()
        return accuracy