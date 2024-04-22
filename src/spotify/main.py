from dotenv import load_dotenv
import os
from auth import SpotifyAuthClient
from user_data import UserData
from playlist_data import PlaylistData
from history_data import HistoryData
from util import format_artist_names

# Load environment variables
load_dotenv()

def main():
    # Read environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    # Scope defines what access we have to the user's data
    scope = 'user-library-read user-top-read playlist-read-private user-read-recently-played'

    # Initialize the SpotifyAuthClient
    spotify_auth_client = SpotifyAuthClient(client_id, client_secret, redirect_uri, scope)
    #spotify_client = spotify_auth_client.get_client()
    try:
        spotify_client = spotify_auth_client.get_client()
        # Continue with the existing setup...
    except Exception as e:
        print(f"Error initializing Spotify client: {str(e)}")
    

    # Instance of UserData to fetch user profile and data
    user_data = UserData(spotify_client)
    user_profile = user_data.get_user_profile()
    print(f"User Profile: {user_profile}")

    # Instance of PlaylistData to fetch user's playlists
    playlist_data = PlaylistData(spotify_client)
    user_playlists = playlist_data.get_user_playlists()
    print(f"User's Playlists: {[playlist['name'] for playlist in user_playlists['items']]}")

    # Instance of HistoryData to fetch recently played tracks
    history_data = HistoryData(spotify_client)
    recently_played = history_data.get_recently_played_tracks()
    print("Recently Played Tracks:")
    for track in recently_played:
        print(f" - {track['track']['name']} by {format_artist_names(track['track']['artists'])}")

if __name__ == '__main__':
    main()