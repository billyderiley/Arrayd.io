from sklearn.preprocessing import StandardScaler
import numpy as np
import torch
import torchaudio.transforms as transforms
import torchaudio

# Set numpy print options to increase threshold for truncation
np.set_printoptions(threshold=np.inf)

def get_waveform_samplerate_mp3(audio_buffer):
    waveform, sample_rate = torchaudio.load(audio_buffer,format='mp3')
    return waveform, sample_rate

# Initialize scalers for Mel spectrogram and spectral centroid
mel_spec_scaler = StandardScaler()
spectral_centroid_scaler = StandardScaler()

def normalize_features(features, scaler):
    # Reshape to (num_samples, num_features) if necessary
    reshaped_features = features.reshape(-1, features.shape[-1])
    #Check for NaN or infinite values
    if np.isnan(reshaped_features).any() or np.isinf(reshaped_features).any():
        print("Warning: Invalid values found in features before normalization.")
        #reshaped_features = np.nan_to_num(reshaped_features)  # Replace NaNs with zero and inf with finite numbers
        raise ValueError("Nan or Zero occured")
    normalized_features = scaler.fit_transform(reshaped_features)
    return normalized_features.reshape(features.shape)

def extract_mel_spec(audio_buffer):
    waveform, sample_rate = get_waveform_samplerate_mp3(audio_buffer)
    n_fft = 2048
    hop_length = 512
    mel_spectrogram_transform = transforms.MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=128,
        normalized=True
    )
    mel_spectrogram = mel_spectrogram_transform(waveform)
    mel_spectrogram = mel_spectrogram.numpy()
    # Normalize the Mel Spectrogram
    mel_spectrogram = normalize_features(mel_spectrogram, mel_spec_scaler)
    return torch.tensor(mel_spectrogram)

def extract_spectral_centroid(audio_buffer):
    waveform, sample_rate = get_waveform_samplerate_mp3(audio_buffer)
    n_fft = 2048
    hop_length = 512
    spectral_centroid_transform = transforms.SpectralCentroid(
        sample_rate=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length
    )
    spectral_centroid = spectral_centroid_transform(waveform)
    spectral_centroid = spectral_centroid.numpy()
    # Normalize the Spectral Centroid
    spectral_centroid = normalize_features(spectral_centroid, spectral_centroid_scaler)
    return torch.tensor(spectral_centroid)
