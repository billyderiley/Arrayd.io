import torchaudio
import torchaudio.transforms as transforms
import numpy as np
# Set numpy print options to increase threshold for truncation
np.set_printoptions(threshold=np.inf)

def extract_audio_features(audio_buffer):
    waveform, sample_rate = torchaudio.load(audio_buffer,format='mp3')
    
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
    print("Waveform is : ", waveform)
    print("Shape of waveoform: ", waveform.shape)
    print("Shape of Mel ", mel_spectrogram.shape)
    return mel_spectrogram