import torchaudio
import torchaudio.transforms as transforms
import numpy as np
# Set numpy print options to increase threshold for truncation
np.set_printoptions(threshold=np.inf)

def get_waveform_samplerate_mp3(audio_buffer):
    waveform, sample_rate = torchaudio.load(audio_buffer,format='mp3')
    return waveform, sample_rate

def extract_audio_features(audio_buffer, feature_type : str):
    waveform, sample_rate = get_waveform_samplerate_mp3(audio_buffer=audio_buffer)
    #feature = extract_mel_spec(waveform, sample_rate)
    
    if feature_type == 'Mel':
        feature = extract_mel_spec(waveform, sample_rate)
    elif feature_type == 'SpectralCentroid':
        feature = extract_spectral_centroid(waveform, sample_rate)
    return feature

def extract_mutiple_audio_features(audio_buffer):
    waveform, sample_rate = get_waveform_samplerate_mp3(audio_buffer=audio_buffer)
    # Extract multiple features
    mel_spectrogram = extract_mel_spec(waveform, sample_rate)
    spectral_centroid = extract_spectral_centroid(waveform, sample_rate)
     # Flatten and concatenate features
    mel_spectrogram_flat = mel_spectrogram.numpy().flatten()
    spectral_centroid_flat = spectral_centroid.numpy().flatten()
    combined_features = np.concatenate([mel_spectrogram_flat, spectral_centroid_flat])

def extract_mel_spec(audio_buffer):
    waveform, sample_rate = get_waveform_samplerate_mp3(audio_buffer)
    # Assuming a default FFT size might be too low, let's increase it
    n_fft = 2048  # Increasing FFT size
    win_length = None  # you can also set this as needed
    hop_length = 512  # typically n_fft / 4
    
    # Creating the Mel Spectrogram with adjusted parameters
    mel_spectrogram_transform = transforms.MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=n_fft,
        win_length=win_length,
        hop_length=hop_length,
        n_mels=128,  # Adjust as necessary, depending on your analysis requirements
        normalized=True
    )
    
    mel_spectrogram = mel_spectrogram_transform(waveform)
    return mel_spectrogram

def extract_spectral_centroid(audio_buffer):
    waveform, sample_rate = get_waveform_samplerate_mp3(audio_buffer)
    # Assuming a default FFT size might be too low, let's increase it
    n_fft = 2048  # Increasing FFT size
    win_length = None  # you can also set this as needed
    hop_length = 512  # typically n_fft / 4
    spectral_centroid_transform = transforms.SpectralCentroid(
        sample_rate=sample_rate,
        n_fft=n_fft,
        win_length=win_length,
        hop_length=hop_length
    )
    return spectral_centroid_transform(waveform)