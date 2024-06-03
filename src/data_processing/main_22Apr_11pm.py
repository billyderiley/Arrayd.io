from download_previews import download_preview
from audio_feature_extraction import extract_audio_features
import pandas as pd

def main():
    # Assume the DataFrame has been loaded from the CSV
    df = pd.read_csv('data/users_tracks_and_playlists.csv')
    total_tracks = len(df)
    
    
    # Process each track
    for index, row in df.iterrows():
        track_id, preview_url = row['track_id'], row['preview_url']
        
        # Download the preview
        audio_buffer, error = download_preview(track_id, preview_url)
        if error:
            print(error)
            continue  # Skip this track and move to the next
        
        # Extract audio features
        features = extract_audio_features(audio_buffer)
        # Do something with the features, like saving them or passing them to a model
        
        # IMPORTANT: Clear the buffer after processing to free memory
        audio_buffer.close()
        
        # Print progress
        progress = (index + 1) / total_tracks * 100  # Calculate progress as a percentage
        print(f"Processing... {progress:.2f}% completed", end='\r')

    print("\nFinished processing tracks.")

if __name__ == '__main__':
    main()
