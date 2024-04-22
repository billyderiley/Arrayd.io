import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAuthClient:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.sp_auth = self.create_spotify_oauth()

    def create_spotify_oauth(self):
        return SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        )

    def get_client(self):
        # Ensure token_info is a dictionary
        token_info = self.sp_auth.get_cached_token()
        if not token_info:
            token_info = self.sp_auth.get_access_token(as_dict=True)  # Make sure this returns a dictionary
        if 'access_token' in token_info:
            return spotipy.Spotify(auth=token_info['access_token'])
        else:
            raise Exception("Failed to retrieve access token.")

# You can create a function that initializes this client with the actual credentials
def initialize_spotify_client(client_id, client_secret, redirect_uri, scope):
    auth_client = SpotifyAuthClient(client_id, client_secret, redirect_uri, scope)
    return auth_client.get_client()
