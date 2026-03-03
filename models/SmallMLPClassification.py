import torch
import torch.nn as nn 

from torch.optim import Adam

class SmallMLPClassification(nn.Module):
    def __init__(self, input_size, num_classes):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )

        self.optimizer = Adam(self.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, input):
        return self.model(input)
    
    def train_model(self, epochs, dataloader):
        self.train()

        for epoch in range(epochs):
            total_loss = 0
            for xb, yb in dataloader:
                preds = self.forward(xb)
                loss = self.criterion(preds, yb)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
            
            avg_loss = total_loss / len(dataloader)
            print(f"Epoch {epoch+1}, Train Loss: {avg_loss:.4f}")
    
    def evaluate(self, dataloader):
        self.eval()
        total_loss = 0

        with torch.no_grad():
            for xb, yb in dataloader:
                preds = self.forward(xb)
                loss = self.criterion(preds, yb)

                total_loss += loss.item()
        
        avg_loss = total_loss / len(dataloader)
        print(f"Loss: {avg_loss:.4f}")