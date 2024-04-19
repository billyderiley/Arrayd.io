# __init__.py in the spotify package

# Define what symbols to export when 'from spotify import *' is used
__all__ = ['authenticate', 'user_data', 'playlist_data', 'track_data', 'history_data', 'util']

# You could also initialize package-level data here, like a shared API client instance:
from .auth import SpotifyAuthClient

# Initialize a SpotifyAuthClient for use in other modules within this package
spotify_auth_client = SpotifyAuthClient(client_id='your_client_id', client_secret='your_client_secret')
