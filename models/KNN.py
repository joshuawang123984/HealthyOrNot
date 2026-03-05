import torch

class KNN:
    def __init__(self, X_train, y_train, k=5):
        self.k = k
        self.X_train = torch.tensor(X_train.values if hasattr(X_train, 'values') else X_train, dtype=torch.float32)
        self.y_train = torch.tensor(y_train.values if hasattr(y_train, 'values') else y_train, dtype=torch.float32).squeeze()
    
    def predict(self, X_test):
        X = torch.tensor(X_test.values if hasattr(X_test, 'values') else X_test, dtype=torch.float32)

        dists = torch.cdist(X, self.X_train)
        topk = torch.topk(dists, self.k, largest=False).indices
        neighbor_labels = self.y_train[topk]

        return neighbor_labels
    def score(self, X_test, y_test):
        neighbor_labels = self.predict(X_test)

        preds = torch.mode(neighbor_labels, dim=1).values

        y = torch.tensor(y_test.values if hasattr(y_test, 'values') else y_test, dtype=torch.float32).squeeze()

        accuracy = (preds == y).float().mean().item()

        return accuracy