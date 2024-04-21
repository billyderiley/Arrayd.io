from spotipy.oauth2 import SpotifyOAuth
import spotipy

class SpotifyAuthClient:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".cache-" + client_id  # This is optional but useful for not having to re-authenticate on every run.
        )

    def get_auth_url(self):
        return self.sp_oauth.get_authorize_url()

    def authenticate_user(self, code):
        # Exchanges the code for a token and caches the token
        token_info = self.sp_oauth.get_access_token(code)
        return spotipy.Spotify(auth=token_info['access_token'])

# The following code is meant to be run interactively:
# auth_client = SpotifyAuthClient('your_client_id', 'your_client_secret', 'your_redirect_uri', 'required_scope')
# auth_url = auth_client.get_auth_url()
# print(f"Please navigate here in your browser: {auth_url}")
# print("Please enter the URL you were redirected to after authorizing the app:")
# response_url = input()
# code = auth_client.sp_oauth.parse_response_code(response_url)
# spotify_client = auth_client.authenticate_user(code)