import pandas as pd
from download_previews import download_preview
from audio_feature_extraction import extract_audio_features
import os

#def populate_feature_data(csv_path='data/users_tracks_and_playlists.csv', output_csv_path='data/feature_data.csv', batch_size=1000):
def populate_feature_data(csv_path='../../spotify/spotify_data/users_tracks_and_playlists.csv', output_csv_path='data/feature_data.csv', batch_size=1000):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(project_root, 'src', 'spotify', 'spotify_data', 'users_tracks_and_playlists.csv')
    full_path = os.path.abspath(csv_path)
    print("Full path to CSV:", full_path)
    df = pd.read_csv(full_path)
    total_tracks = len(df)
    
    features_list = []
    batch_count = 0
    limit = 0

    for index, row in df.iterrows():
        track_id, preview_url = row['track_id'], row['preview_url']
        
        audio_buffer, error = download_preview(track_id, preview_url)
        if error:
            print(error)
            continue
        
        features = extract_audio_features(audio_buffer)
        audio_buffer.close()
        
        features_list.append({
            'track_id': track_id,
            'features': features.numpy().flatten(),
            'in_playlist_ids': row['in_playlist_ids']
        })
        print(f"len of features list {features_list}")
        if len(features_list) <= batch_size:
            print("adding to dataframe\n")
            temp_df = pd.DataFrame(features_list)
            if batch_count == 0:
                temp_df.to_csv(output_csv_path, index=False, mode='w')
            else:
                temp_df.to_csv(output_csv_path, index=False, mode='a', header=False)
            features_list = []  # Clear list after saving
            batch_count += 1
        else:
            print("not adding to dataframe\n")
        
        progress = ((index + 1) / total_tracks) * 100
        print(f"Processing... {progress:.2f}% completed", end='\r')

    # Save any remaining data
    if features_list:
        temp_df = pd.DataFrame(features_list)
        temp_df.to_csv(output_csv_path, index=False, mode='a', header=False if batch_count > 0 else True)
    print("\nFinished processing tracks.")

