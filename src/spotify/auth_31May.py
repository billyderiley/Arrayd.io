import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Load existing .env file or create one if it doesn't exist
load_dotenv()

class SpotifyAuthClient:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        self.scope = 'user-library-read user-top-read playlist-read-private user-read-recently-played'

        # Prompt for credentials if not found
        if not self.client_id or not self.client_secret or not self.redirect_uri:
            self.prompt_for_credentials()

        self.sp_auth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        )

    def prompt_for_credentials(self):
        print("Spotify API credentials not found. Please enter your credentials.")
        self.client_id = input("Enter your Spotify Client ID: ")
        self.client_secret = input("Enter your Spotify Client Secret: ")
        self.redirect_uri = input("Enter your Spotify Redirect URI: ")

        # Save the provided credentials into .env file for later use
        with open('.env', 'a') as f:
            f.write(f"SPOTIFY_CLIENT_ID={self.client_id}\n")
            f.write(f"SPOTIFY_CLIENT_SECRET={self.client_secret}\n")
            f.write(f"SPOTIFY_REDIRECT_URI={self.redirect_uri}\n")

    def get_client(self):
        token_info = self.sp_auth.get_cached_token()
        if token_info:
            print("got a token")
        if not token_info:
            token_info = self.sp_auth.get_access_token(as_dict=True)
        if 'access_token' in token_info:
            return spotipy.Spotify(auth=token_info['access_token'])
        else:
            raise Exception("Failed to retrieve access token.")