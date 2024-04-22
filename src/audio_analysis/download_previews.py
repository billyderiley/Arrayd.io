import requests
import io

def download_preview(track_id, preview_url):
    if not preview_url:
        return None, "No preview URL provided."
    
    response = requests.get(preview_url)
    if response.status_code == 200:
        # Using a bytes buffer to hold the audio data
        audio_buffer = io.BytesIO(response.content)
        return audio_buffer, None
    else:
        return None, f"Failed to download preview for track ID {track_id}"
