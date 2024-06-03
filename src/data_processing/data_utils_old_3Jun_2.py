import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from src.data_processing.download_previews import download_preview
from src.data_processing.audio_feature_extraction import extract_audio_features
import numpy as np

class AudioDataset(Dataset):
    def __init__(self, data_frame):
        self.data_frame = data_frame
    
    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        # Calculate and print progress
        progress = ((idx + 1) / len(self.data_frame)) * 100  # Update progress
        print(f"Processing... {progress:.2f}% completed", end='\r')

        row = self.data_frame.iloc[idx]
        preview_url = row['preview_url']

        # Initialize labels; assume 'in_playlist_ids' contains integer labels or a semicolon-separated list of ids
        # We need to process it to extract a single label for training
        label_ids = row['in_playlist_ids'].split(';')  # Assuming multiple ids can be present
        label_id = int(label_ids[0])  # Take the first one as the label

        # Download and extract features on-the-fly
        audio_buffer, error = download_preview(row['track_id'], preview_url)
        if error:
            print(f"Error downloading audio for track ID {row['track_id']}: {error}")
            # Return a dummy tensor for features and label if error occurs
            return torch.zeros(1), torch.tensor(label_id, dtype=torch.int64)

        # Extract audio features
        features = extract_audio_features(audio_buffer)
        audio_buffer.close()

        # Convert features to a tensor
        feature_tensor = torch.tensor(features.numpy().flatten(), dtype=torch.float32)

        return feature_tensor, torch.tensor(label_id, dtype=torch.int64)

        
"""    def __getitem__(self, idx):
        # Calculate and print progress
        progress = ((idx + 1) / len(self.data_frame)) * 100  # Update progress
        print(f"Processing... {progress:.2f}% completed", end='\r')
        
        row = self.data_frame.iloc[idx]
        preview_url = row['preview_url']
        
        # Download and extract features on-the-fly
        audio_buffer, error = download_preview(row['track_id'], preview_url)
        if error:
            print(f"Error downloading audio for track ID {row['track_id']}: {error}")
            return torch.tensor([]), row['in_playlist_ids']  # Handle error by returning an empty tensor

        # Extract audio features
        features = extract_audio_features(audio_buffer)
        audio_buffer.close()

        # Convert features to a tensor
        feature_tensor = torch.tensor(features.numpy().flatten(), dtype=torch.float32)
        
        return feature_tensor, row['in_playlist_ids']"""

def load_data(csv_path):
    """Load data from a CSV file."""
    df = pd.read_csv(csv_path)
    return df

def create_dataloader(df, batch_size=32, shuffle=True):
    """Create a DataLoader from a DataFrame and calculate the total number of batches."""
    dataset = AudioDataset(df)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    total_batches = (len(dataset) + batch_size - 1) // batch_size  # Calculate total number of batches
    return dataloader, total_batches


# Example usage:
# dataset = AudioDataset('path_to_your_csv.csv')
# loader = torch.utils.data.DataLoader(dataset, batch_size=10, shuffle=True)
