import pandas as pd
from download_previews import download_preview
from audio_feature_extraction import extract_audio_features
from save_feature_data_to_csv import save_feature_data_to_csv  # Import the save function

def populate_feature_data(csv_path='data/users_tracks_and_playlists.csv', output_csv_path='data/feature_data.csv'):
    df = pd.read_csv(csv_path)
    total_tracks = len(df)
    
    # Prepare a DataFrame to store the features
    feature_data = pd.DataFrame()

    for index, row in df.iterrows():
        track_id, preview_url = row['track_id'], row['preview_url']
        
        # Download the preview
        audio_buffer, error = download_preview(track_id, preview_url)
        if error:
            print(f"Error for track ID {track_id}: {error}")
            continue  # Skip this track and move to the next
        
        # Extract audio features
        features = extract_audio_features(audio_buffer)
        audio_buffer.close()
        
        # Append features and track info to the DataFrame
        feature_data = feature_data.append({
            'track_id': track_id,
            'features': features.numpy().flatten(),  # Assuming features are a tensor and you flatten it
            'in_playlist_ids': row['in_playlist_ids']  # Or any other relevant data
        }, ignore_index=True)

        progress = (index + 1) / total_tracks * 100  # Calculate progress as a percentage
        print(f"Processing... {progress:.2f}% completed", end='\r')

    # Use the separate script to save the feature data to CSV
    save_feature_data_to_csv(feature_data, output_csv_path)
    print("\nFinished processing tracks.")

