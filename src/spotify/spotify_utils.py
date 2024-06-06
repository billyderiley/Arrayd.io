import sys
sys.path.append(r'/workspaces/Arrayd.io')

from src.data_processing.audio_feature_extraction import get_waveform_samplerate_mp3

def check_download_duration(audio_buffer):
    waveform, sample_rate = get_waveform_samplerate_mp3(audio_buffer)
    duration = waveform.shape[1] / sample_rate
    return duration