import torch.nn as nn

def get_model(input_size, num_classes):
    model = nn.Sequential(
        nn.Linear(input_size, 512),  # First layer adjusts according to input size
        nn.ReLU(),
        nn.Linear(512, 128),
        nn.ReLU(),
        nn.Linear(128, num_classes),
        nn.LogSoftmax(dim=1)
    )
    return model
