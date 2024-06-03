import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from src.data_processing.download_previews import download_preview
from src.data_processing.audio_feature_extraction import extract_audio_features
import numpy as np

class AudioDataset(Dataset):
    def __init__(self, data_frame, playlist_to_idx):
        self.data_frame = data_frame
        self.playlist_to_idx = playlist_to_idx
    
    def __len__(self):
        return len(self.data_frame)
    
    def __getitem__(self, idx):
        row = self.data_frame.iloc[idx]
        preview_url = row['preview_url']
        audio_buffer, error = download_preview(row['track_id'], preview_url)
        if error:
            print(f"Error downloading audio for track ID {row['track_id']}: {error}")
            return torch.tensor([]), row['in_playlist_ids']
        features = extract_audio_features(audio_buffer)
        audio_buffer.close()
        feature_tensor = torch.tensor(features.numpy().flatten(), dtype=torch.float32)
        label_tensor = self.encode_labels(row['in_playlist_ids'])
        return feature_tensor, label_tensor

    def encode_labels(self, playlist_ids):
        labels = np.zeros(len(self.playlist_dict))
        indices = [self.playlist_dict[id] for id in playlist_ids.split(';') if id in self.playlist_dict]
        labels[indices] = 1
        return labels
"""
    def __getitem__(self, idx):
        row = self.data_frame.iloc[idx]
        preview_url = row['preview_url']

        audio_buffer, error = download_preview(row['track_id'], preview_url)
        if error:
            print(f"Error downloading audio for track ID {row['track_id']}: {error}")
            return torch.tensor([]), torch.tensor(-1)  # Return -1 as a dummy label for error cases

        features = extract_audio_features(audio_buffer)
        audio_buffer.close()

        feature_tensor = torch.tensor(features.numpy().flatten(), dtype=torch.float32)
        
        # Convert playlist ID to an index
        label_id = self.playlist_to_idx.get(row['in_playlist_ids'], -1)  # Default to -1 if not found
        return feature_tensor, torch.tensor(label_id, dtype=torch.int64)"""
    
def load_data(csv_path):
    """Load data from a CSV file."""
    df = pd.read_csv(csv_path)
    return df

def create_dataloader(df, batch_size=32, shuffle=True):
    """Create a DataLoader from a DataFrame and calculate the total number of batches."""
    unique_playlists = df['in_playlist_ids'].unique()
    playlist_to_idx = {pid: idx for idx, pid in enumerate(unique_playlists)}
    dataset = AudioDataset(df, playlist_to_idx)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    total_batches = (len(dataset) + batch_size - 1) // batch_size  # Calculate total number of batches
    return dataloader, total_batches

