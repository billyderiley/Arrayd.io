from pydub import AudioSegment
import io
import torchaudio

def convert_mp3_to_wav(mp3_data):
    # Load MP3 into pydub
    audio = AudioSegment.from_file(io.BytesIO(mp3_data), format="mp3")
    # Convert to WAV
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)  # Rewind to the beginning of the BytesIO object
    return wav_io

def extract_audio_features(audio_buffer):
    # Convert the MP3 BytesIO to WAV BytesIO
    wav_io = convert_mp3_to_wav(audio_buffer.getvalue())
    
    # Load the WAV BytesIO with torchaudio
    waveform, sample_rate = torchaudio.load(wav_io)
    return waveform, sample_rate
