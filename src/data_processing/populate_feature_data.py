import pandas as pd
from download_previews import download_preview
from audio_feature_extraction import extract_audio_features
import os
from dotenv import load_dotenv

load_dotenv()

def populate_feature_data(csv_path, output_csv_path=None, batch_size=1000, save_to_csv=False):
    df = pd.read_csv(csv_path)
    total_tracks = len(df)
    
    features_list = []
    batch_count = 0

    for index, row in df.iterrows():
        track_id, preview_url = row['track_id'], row['preview_url']
        
        audio_buffer, error = download_preview(track_id, preview_url)
        if error:
            print(f"Error downloading preview: {error}")
            continue
        
        features = extract_audio_features(audio_buffer)
        audio_buffer.close()
        
        features_list.append({
            'track_id': track_id,
            'features': features.numpy().flatten().tolist(),  # Convert numpy array to list
            'in_playlist_ids': row['in_playlist_ids']
        })

        if len(features_list) >= batch_size:
            if save_to_csv and output_csv_path:
                print(f"Saving batch {batch_count + 1} to CSV...")
                temp_df = pd.DataFrame(features_list)
                if batch_count == 0:
                    temp_df.to_csv(output_csv_path, index=False, mode='w')
                else:
                    temp_df.to_csv(output_csv_path, index=False, mode='a', header=False)
                batch_count += 1
            features_list = []  # Clear list after saving or processing
            
        progress = ((index + 1) / total_tracks) * 100
        print(f"Processing... {progress:.2f}% completed", end='\r')

    # Save any remaining data
    if features_list and save_to_csv and output_csv_path:
        print("Saving final batch to CSV...")
        temp_df = pd.DataFrame(features_list)
        temp_df.to_csv(output_csv_path, index=False, mode='a', header=False if batch_count > 0 else True)

    print("\nFinished processing tracks.")

# Example usage:
if __name__ == "__main__":
    populate_feature_data(
        csv_path='../../spotify/spotify_data/users_tracks_and_playlists.csv',
        output_csv_path='data/feature_data.csv',
        save_to_csv=True  # Toggle this to False if you do not want to save to CSV
    )