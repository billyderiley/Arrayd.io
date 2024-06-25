import torch
from torch.utils.data import DataLoader
from model import get_model
from torch import nn
from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss

def train_initial_model(dataloader, input_size, num_classes):
    """
    Train an initial supervised model using labeled data.
    
    Parameters:
    dataloader (DataLoader): DataLoader for the labeled data
    input_size (int): The size of the input features
    num_classes (int): Number of classes (playlists)
    
    Returns:
    model (nn.Module): Trained PyTorch model
    """
    model = get_model(input_size, num_classes)
    optimizer = Adam(model.parameters(), lr=0.001)
    loss_fn = BCEWithLogitsLoss()

    for features, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(features)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        print(f"Labeled Loss: {loss.item()}")
    
    return model

def predict_unlabeled(model, dataloader):
    """
    Predict labels for the unlabeled data using the trained model.
    
    Parameters:
    model (nn.Module): Trained PyTorch model
    dataloader (DataLoader): DataLoader for the unlabeled data
    
    Returns:
    list: Predicted labels for the unlabeled data
    """
    model.eval()
    predictions = []
    with torch.no_grad():
        for features in dataloader:
            outputs = model(features)
            predictions.append(outputs)
    return torch.cat(predictions)

def self_training(labeled_dataloader, unlabeled_dataloader, input_size, num_classes):
    """
    Perform self-training by iteratively refining the model using labeled and pseudo-labeled data.
    
    Parameters:
    labeled_dataloader (DataLoader): DataLoader for labeled data
    unlabeled_dataloader (DataLoader): DataLoader for unlabeled data
    input_size (int): The size of the input features
    num_classes (int): Number of classes (playlists)
    
    Returns:
    model (nn.Module): Refined PyTorch model
    """
    model = train_initial_model(labeled_dataloader, input_size, num_classes)
    pseudo_labels = predict_unlabeled(model, unlabeled_dataloader)
    
    combined_features = torch.cat([labeled_dataloader.dataset.tensors[0], unlabeled_dataloader.dataset.tensors[0]])
    combined_labels = torch.cat([labeled_dataloader.dataset.tensors[1], pseudo_labels])
    
    combined_dataloader = DataLoader(list(zip(combined_features, combined_labels)), batch_size=32, shuffle=True)
    optimizer = Adam(model.parameters(), lr=0.0001)
    loss_fn = BCEWithLogitsLoss()

    for features, labels in combined_dataloader:
        optimizer.zero_grad()
        outputs = model(features)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        print(f"Combined Loss: {loss.item()}")

    return model
