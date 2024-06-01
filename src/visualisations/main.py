from load_features import load_features, get_tracks_by_id, get_tracks_by_playlist_id
from mel_spec_visualisation import plot_mel_spectrogram
import pandas as pd

def display_menu(items, item_type="track"):
    for index, item in enumerate(items, 1):
        if item_type == "track":
            print(f"{index}. Track ID: {item}")
        elif item_type == "playlist":
            print(f"{index}. Playlist ID: {item}")

def get_user_selections(items):
    selections = []
    while True:
        try:
            choice = input("Enter the number to select (leave blank and press enter to finish): ").strip()
            if choice == "":
                break
            index = int(choice) - 1
            if 0 <= index < len(items):
                selections.append(items[index])
            else:
                print("Invalid number, please try again.")
        except ValueError:
            print("Please enter a valid number.")
    return selections

def main():
    print("Loading feature data...")
    df = load_features()  # Load the full dataset

    choice = input("Enter '1' to search by track ID or '2' to search by playlist ID: ").strip()

    if choice == '1':
        unique_tracks = df['track_id'].unique().tolist()
        print("Available Tracks:")
        display_menu(unique_tracks, "track")
        selected_track_ids = get_user_selections(unique_tracks)
        tracks = get_tracks_by_id(df, selected_track_ids)

    elif choice == '2':
        # Assuming playlist IDs can be extracted from the column as unique values
        df['in_playlist_ids'] = df['in_playlist_ids'].apply(lambda x: x.split(';'))
        unique_playlists = sorted(set(playlist_id for sublist in df['in_playlist_ids'] for playlist_id in sublist))
        print("Available Playlists:")
        display_menu(unique_playlists, "playlist")
        selected_playlist_ids = get_user_selections(unique_playlists)
        tracks = pd.concat([get_tracks_by_playlist_id(df, pid) for pid in selected_playlist_ids], ignore_index=True)

    else:
        print("Invalid choice.")
        return

    if tracks.empty:
        print("No tracks found for the selection.")
        return

    for _, row in tracks.iterrows():
        track_id = row['track_id']
        features = row['features']
        plot_mel_spectrogram(track_id, features, f"Mel Spectrogram for Track ID {track_id}")

if __name__ == "__main__":
    main()
