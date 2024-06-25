from dotenv import load_dotenv
import os
from auth import SpotifyAuthClient
from user_data import UserData
from populate_data import create_tracks_dataframe
from playlist_data import PlaylistData
from save_user_playlist_data_to_csv import save_dataframe_to_csv


# Load environment variables
load_dotenv()

def print_summary(user_profile, user_playlists):
    print("_" * 80)
    print("User Summary")
    print("-" * 80)
    print(f"Name: {user_profile['display_name']}")
    print(f"UserID: {user_profile['id']}")
    #print("Number of playlists in total: ", len(user_playlists['items']))
    print("Number of playlists in total: ", len(user_playlists))
    counter = 0
    #for playlist in user_playlists['items']:
    for playlist in user_playlists:
        print(f"Playlist Name: {playlist['name']} | Playlist ID: {playlist['id']} | Tracks: {playlist['tracks']['total']}")
        counter+=1
        print(counter)
    print("_" * 80)

def main():
    # Initialize the SpotifyAuthClient
    spotify_auth_client = SpotifyAuthClient()
    spotify_client = spotify_auth_client.get_client()

    # Fetch user data and print summary
    user_data = UserData(spotify_client)
    user_profile = user_data.get_user_profile()

    # Initialize PlaylistData to fetch user's playlists
    playlist_data = PlaylistData(spotify_client)
    user_playlists = playlist_data.get_user_playlists()
    print("All user playlists: ")
    print_summary(user_profile, user_playlists)
    #for playlist in user_playlists['items']:
    #    print(playlist['name'])
    # Configurable exclusion criteria
    exclude_names = ["Crate Digging", "Latest"]
    max_tracks = 270
    min_tracks = 210
    limit = None
    # Fetch playlists with exclusions
    #user_playlists_with_exclusions = playlist_data.get_user_playlists(limit=limit, exclude_names=exclude_names, max_tracks=max_tracks)
    print(exclude_names, len(exclude_names))
    filtered_playlists = playlist_data.filter_user_playlists(user_playlists, exclude_names, min_tracks, max_tracks)
    
    #for playlist in filtered_playlists['items']:
    for playlist in filtered_playlists:
        print(f"Playlist: {playlist['name']} has {playlist['tracks']['total']} tracks")

    # Print summary
    print("User playlists included: ")
    print_summary(user_profile, filtered_playlists)

    #exit()

    # Populate DataFrame with track data
    #tracks_df = create_tracks_dataframe(spotify_client=spotify_client, limit=max_playlists, exclude_names=exclude_names, max_tracks=max_tracks)
    tracks_df = create_tracks_dataframe(filtered_playlists, spotify_client)
    # For demo purposes, print the DataFrame shape and first few rows
    print(f"DataFrame Shape: {tracks_df.shape}")
    #print(tracks_df.head())

    # Now save the DataFrame to CSV
    save_dataframe_to_csv(tracks_df)

if __name__ == '__main__':
    main()