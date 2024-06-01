import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def load_features(csv_path=os.getenv('AUDIO_ANALYSIS_OUTPUT_CSV_PATH')):
    df = pd.read_csv(csv_path)
    # Simple script to check the content of the CSV file
    print(df.head(10))
    print(df.features[0].split())
    return df

def get_tracks_by_id(df, track_ids):
    # Assume track_ids is a list of IDs
    return df[df['track_id'].isin(track_ids)]

def get_tracks_by_playlist_id(df, playlist_id):
    # This function filters rows where the playlist_id appears in the 'in_playlist_id' column
    mask = df['in_playlist_ids'].apply(lambda x: playlist_id in x.split(';'))
    return df[mask]

# Example usage
if __name__ == "__main__":
    df = load_features()
    specific_tracks = get_tracks_by_id(df, ['track_id1', 'track_id2'])
    playlist_tracks = get_tracks_by_playlist_id(df, 'playlist_id1')
