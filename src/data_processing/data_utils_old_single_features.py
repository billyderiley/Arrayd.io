import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from src.data_processing.download_previews import download_preview
from src.data_processing.audio_feature_extraction import extract_audio_features, extract_mutiple_audio_features
from src.storage_access.file_storage import check_track_id_has_30_second_preview_downloaded, retrieve_download
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
        track_id = row['track_id']
        if check_track_id_has_30_second_preview_downloaded(track_id) is True:
            audio_buffer = retrieve_download(track_id)
            close_buffer = False
        else:
            audio_buffer, error = download_preview(row['track_id'], preview_url)
            close_buffer = True
        features = extract_audio_features(audio_buffer)
        audio_buffer.close() if close_buffer is True else None
        feature_tensor = torch.tensor(features.numpy().flatten(), dtype=torch.float32)
        #print(f"feature size is {feature_tensor.size()}")
        label_tensor = self.encode_labels(row['in_playlist_ids'])
        return feature_tensor, label_tensor

    def encode_labels(self, playlist_ids):
        labels = np.zeros(len(self.playlist_to_idx))
        indices = [self.playlist_to_idx[id] for id in playlist_ids.split(';') if id in self.playlist_to_idx]
        labels[indices] = 1
        return torch.tensor(labels, dtype=torch.float32)
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

def create_dataloader(df, playlist_to_idx, batch_size=32, shuffle=True):
    """Create a DataLoader from a DataFrame."""
    dataset = AudioDataset(df, playlist_to_idx)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle), len(dataset)

def create_dataloader_multi_features(df, playlist_to_idx, batch_size=32, shuffle=True):
    """Create a DataLoader from a DataFrame."""
    dataset = AudioDatasetMultiFeatures(df, playlist_to_idx)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle), len(dataset)


class AudioDatasetMultiFeatures(Dataset):
    def __init__(self, data_frame):
        self.data_frame = data_frame
    
    def __len__(self):
        return len(self.data_frame)
    
    def __getitem__(self, idx):
        row = self.data_frame.iloc[idx]
        preview_url = row['preview_url']
        track_id = row['track_id']
        if check_track_id_has_30_second_preview_downloaded(track_id) is True:
            audio_buffer = retrieve_download(track_id)
            close_buffer = False
        else:
            audio_buffer, error = download_preview(row['track_id'], preview_url)
            close_buffer = True
        mutiple_features = extract_mutiple_audio_features(audio_buffer)
        audio_buffer.close() if close_buffer is True else None
        feature_tensor = torch.tensor(mutiple_features, dtype=torch.float32)
        label_tensor = self.encode_labels(row['in_playlist_ids'])
        
        return feature_tensor, label_tensor
