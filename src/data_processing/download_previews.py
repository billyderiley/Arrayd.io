import sys
sys.path.append(r'/workspaces/Arrayd.io')

import requests
import pandas as pd
import io
from src.data_processing.bot_detection import get_random_headers, get_proxy, proxy_auth, update_data_usage, get_total_data_used, random_delay

def download_preview(track_id, preview_url):
    # Check if the URL is a NaN value or seems invalid
    if pd.isna(preview_url) or not isinstance(preview_url, str) or not preview_url.startswith('http'):
        return None, f"No valid URL provided for track ID {track_id}"
    
    headers = get_random_headers()
    proxy = get_proxy()

    try:
        #response = requests.get(preview_url, headers=headers, proxies=proxy, auth=proxy_auth)
        response = requests.get(preview_url, headers=headers, auth=proxy_auth)
        if response.status_code == 200:
            audio_buffer = io.BytesIO(response.content)
            # store_download(audio_buffer, track_id)
            # Track the amount of data used
            data_used = len(response.content)
            update_data_usage(data_used)
            return audio_buffer, None
        else:
            return None, f"Failed to download preview for track ID {track_id}: HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, str(e)
    finally:
        # Random delay to mimic human behavior
        random_delay()

# Example usage
if __name__ == "__main__":
    track_id = 1
    preview_url = 'https://example.com/audio.mp3'
    audio_buffer, error = download_preview(track_id, preview_url)
    if audio_buffer:
        print("Download successful")
    else:
        print(f"Error: {error}")

    print(f"Total data used: {get_total_data_used():.2f} MB")
