import requests
import pandas as pd
import io

def download_preview(track_id, preview_url):
    # Check if the URL is a NaN value or seems invalid
    if pd.isna(preview_url) or not isinstance(preview_url, str) or not preview_url.startswith('http'):
        return None, f"No valid URL provided for track ID {track_id}"

    try:
        response = requests.get(preview_url)
        if response.status_code == 200:
            check_preview_size(io.BytesIO(response.content))
            return io.BytesIO(response.content), None
        else:
            return None, f"Failed to download preview for track ID {track_id}: HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, str(e)

def check_preview_size(preview_audio_buffer):
    print("audio buffer object is: ", preview_audio_buffer.si)
