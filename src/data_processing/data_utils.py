import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from src.data_processing.download_previews import download_preview
from src.data_processing.audio_feature_extraction import extract_spectral_centroid, extract_mel_spec
from src.storage_access.file_storage import check_track_id_has_30_second_preview_downloaded, retrieve_download
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from src.data_processing.download_previews import download_preview
from src.data_processing.audio_feature_extraction import extract_spectral_centroid
from src.storage_access.file_storage import check_track_id_has_30_second_preview_downloaded, retrieve_download, store_download
import numpy as np

class AudioDataset(Dataset):
    def __init__(self, data_frame, features=['mel_spectrogram', 'spectral_centroid']):
        self.data_frame = data_frame
        self.features = features
        self.playlist_to_idx, self.idx_to_playlist = self.create_playlist_mappings()

    def __len__(self):
        return len(self.data_frame)

    def create_playlist_mappings(self):
        playlists = set()
        self.data_frame['in_playlist_ids'].str.split(';').apply(playlists.update)
        playlist_to_idx = {playlist: idx for idx, playlist in enumerate(playlists)}
        idx_to_playlist = {idx: playlist for playlist, idx in playlist_to_idx.items()}
        return playlist_to_idx, idx_to_playlist

    def __getitem__(self, idx):
        row = self.data_frame.iloc[idx]
        preview_url = row['preview_url']
        track_id = row['track_id']
        print(row['track_id'], row['name'], row['artists'])
        if check_track_id_has_30_second_preview_downloaded(track_id):
            audio_buffer = retrieve_download(track_id)
        else:
            audio_buffer, error = download_preview(track_id, preview_url)
            if error:
                print(f"Error downloading audio for track ID {track_id}: {error}")
                return torch.tensor([]), torch.tensor([])  # Handle error by returning empty tensors
            #store_download(audio_buffer, track_id)
            

        #waveform, sample_rate = extract_audio_features(audio_buffer)

        # Extract different features
        feature_list = []
        if 'mel_spectrogram' in self.features:
            mel_spec = extract_mel_spec(audio_buffer)
            feature_list.append(mel_spec.numpy().flatten())
        if 'spectral_centroid' in self.features:
            spectral_centroid = extract_spectral_centroid(audio_buffer)
            feature_list.append(spectral_centroid.numpy().flatten())
        
        # Concatenate all features
        feature_tensor = torch.tensor(np.concatenate(feature_list), dtype=torch.float32)
        label_tensor = self.encode_labels(row['in_playlist_ids'])
        
        return feature_tensor, label_tensor

    def encode_labels(self, playlist_ids):
        label_ids = playlist_ids.split(';')
        labels = np.zeros(len(self.playlist_to_idx))
        for pid in label_ids:
            if pid in self.playlist_to_idx:
                labels[self.playlist_to_idx[pid]] = 1
        return torch.tensor(labels, dtype=torch.float32)

    def infer_input_size(self):
        # Perform a dummy run to infer the input size
        sample_row = self.data_frame.iloc[0]
        preview_url = sample_row['preview_url']
        track_id = sample_row['track_id']

        if check_track_id_has_30_second_preview_downloaded(track_id):
            audio_buffer = retrieve_download(track_id)
        else:
            audio_buffer, error = download_preview(track_id, preview_url)
            if error:
                raise ValueError(f"Error downloading audio for track ID {track_id}: {error}")

        #waveform, sample_rate = extract_audio_features(audio_buffer)
        
        feature_list = []
        if 'mel_spectrogram' in self.features:
            mel_spec = extract_mel_spec(audio_buffer)
            feature_list.append(mel_spec.numpy().flatten())
        if 'spectral_centroid' in self.features:
            spectral_centroid = extract_spectral_centroid(audio_buffer)
            feature_list.append(spectral_centroid.numpy().flatten())

        input_size = np.concatenate(feature_list).shape[0]
        return input_size

def load_data(csv_path):
    """Load data from a CSV file."""
    df = pd.read_csv(csv_path)
    return df

def create_dataloader(df, batch_size=32, shuffle=True):
    """Create a DataLoader from a DataFrame."""
    dataset = AudioDataset(df)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    total_batches = len(dataloader)
    return dataloader, total_batches, dataset

def num_of_classes_from_unique_playlists(df):
    all_playlists = set()
    def update_unique(value):
        id = value.split(";")
        all_playlists.update(id)
    df['in_playlist_ids'].apply(update_unique)
    unique_count = len(all_playlists)
    print(f'Number of unique classes will be {unique_count}, matching the  number of unique playlist ids')
    return unique_count, all_playlists
