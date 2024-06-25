import sys
sys.path.append(r'/workspaces/Arrayd.io')

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
            audio_buffer = io.BytesIO(response.content)
            #store_download(audio_buffer, track_id)
            return audio_buffer, None
        else:
            return None, f"Failed to download preview for track ID {track_id}: HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, str(e)
    
