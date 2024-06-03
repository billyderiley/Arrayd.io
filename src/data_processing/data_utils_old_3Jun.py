import pandas as pd
from torch.utils.data import DataLoader, Dataset
import numpy as np
import torch

class AudioDataset(Dataset):
    """Custom PyTorch Dataset to load audio features directly."""
    def __init__(self, df):
        self.df = df

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        features = np.array(row['features'])  # Assuming 'features' are stored in an appropriate format
        track_id = row['track_id']            # Assuming each row has a 'track_id'
        return torch.tensor(features, dtype=torch.float32), track_id

def load_data(csv_path):
    """Load data from a CSV file."""
    df = pd.read_csv(csv_path)
    return df

def create_dataloader(df, batch_size=32, shuffle=True):
    """Create a DataLoader from a DataFrame."""
    dataset = AudioDataset(df)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
