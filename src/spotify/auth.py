import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
import spotipy

# Load existing .env file or create one if it doesn't exist
load_dotenv()
class SpotifyAuthClient:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        self.scope = 'user-library-read user-top-read playlist-read-private user-read-recently-played'
        self.sp_auth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path='token_info.cache'  # Path to save the token information
        )

    def get_client(self):
        # Attempt to get a valid Spotify client
        token_info = self.sp_auth.get_cached_token()
        if not token_info:
            # No valid token, need to re-authenticate
            self.prompt_for_reauthentication()
        return spotipy.Spotify(auth_manager=self.sp_auth)

    def prompt_for_reauthentication(self):
        print("Authentication required. Redirecting to Spotify's login page...")
        auth_url = self.sp_auth.get_authorize_url()
        print("Please navigate to the following URL to authorize this application:")
        print(auth_url)
        response = input("Paste the URL you were redirected to here: ")
        code = self.sp_auth.parse_response_code(response)
        token_info = self.sp_auth.get_access_token(code, as_dict=True)  # Exchange code for token
        if 'access_token' not in token_info:
            raise Exception("Failed to retrieve access token.")