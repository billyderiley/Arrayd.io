import torch
from torch.utils.data import DataLoader
from model import get_model

from torch import nn
from torch.optim import Adam
from torch.nn import CrossEntropyLoss

def train_model(dataloader, input_size, num_classes):
    model = get_model(input_size, num_classes)
    optimizer = Adam(model.parameters(), lr=0.001)
    loss_fn = BCEWithLogitsLoss()

    for features, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(features)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()

        print(f"Loss: {loss.item()}")
    return model

class MultiLabelModel(nn.Module):
    def __init__(self, num_features, num_labels):
        super().__init__()
        self.fc = nn.Linear(num_features, num_labels)
    
    def forward(self, x):
        return torch.sigmoid(self.fc(x))  # Sigmoid for binary classification per label

def get_model(input_size, num_classes):
    return MultiLabelModel(input_size, num_classes)