import os

def store_download(audio_buffer, track_id, directory='audio_files'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f"{track_id}.mp3")
    with open(file_path, 'wb') as audio_file:
        audio_file.write(audio_buffer.getbuffer())
    
    return file_path