import os

def store_download(audio_buffer, track_id, directory='temp_30_sec_audio_files'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f"{track_id}.mp3")
    with open(file_path, 'wb') as audio_file:
        audio_file.write(audio_buffer.getbuffer())
    return file_path

def retrieve_download(track_id, directory='temp_30_sec_audio_files'):
    file_path = os.path.join(directory, f"{track_id}.mp3")
    with open(file_path, 'rb') as audio_file:
        audio_buffer = audio_file.read()
    return audio_buffer

def check_track_id_has_30_second_preview_downloaded(track_id, directory='temp_30_sec_audio_files'):
    file_path = os.path.join(directory, f"{track_id}.mp3")
    if not os.path.exists(file_path):
        return False
    else:
        return True

