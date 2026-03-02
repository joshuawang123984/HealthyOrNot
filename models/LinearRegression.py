import torch
import torch.nn as nn 

class LinearRegressionModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1)
    
    def forward(self, x):
        return self.linear(x)

class LinearRegression:
    def __init__(self, X_train, y_train, alpha, epochs=10000, lr=0.0001, lasso=False, ridge=False):
        input_dim = X_train.shape[1]
        self.model = LinearRegressionModel(input_dim)
        self.fit(X_train, y_train, alpha, epochs, lr, lasso, ridge)
    
    def fit(self, X_train, y_train, alpha, epochs, lr, lasso=False, ridge=False):
        X = torch.tensor(X_train.values if hasattr(X_train, 'values') else X_train, dtype=torch.float32)
        y = torch.tensor(y_train.values if hasattr(y_train, 'values') else y_train, dtype=torch.float32).squeeze().unsqueeze(1)

        self.X_mean = X.mean(0)
        self.X_std = X.std(0) + 1e-8
        X = (X - self.X_mean) / self.X_std

        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        loss_fn = nn.MSELoss()

        for _ in range(epochs):
            self.model.train()
            optimizer.zero_grad()

            loss = loss_fn(self.model(X), y)
            if lasso:
                loss += alpha * sum(torch.sum(torch.abs(p)) for p in self.model.parameters())
            elif ridge:
                loss += alpha * sum(torch.sum((p ** 2) for p in self.model.parameters()))

            loss.backward()
            optimizer.step()
    
    def score(self, X_test, y_test):
        X = torch.tensor(X_test.values if hasattr(X_test, 'values') else X_test, dtype=torch.float32)
        y = torch.tensor(y_test.values if hasattr(y_test, 'values') else y_test, dtype=torch.float32).squeeze().unsqueeze(1)

        X = (X - self.X_mean) / self.X_std

        self.model.eval()
        with torch.no_grad():
            preds = self.model(X)
        
        SS_res = torch.sum((y - preds) ** 2)
        SS_tot = torch.sum((y - y.mean()) ** 2)

        r_squared = (1 - (SS_res / SS_tot)).item()
        return r_squared