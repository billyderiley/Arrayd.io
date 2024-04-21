import spotipy
from spotipy.oauth2 import SpotifyOAuth

class HistoryData:
    def __init__(self, spotify_client):
        """Initialize with an authenticated Spotipy client."""
        self.spotify_client = spotify_client

    def get_recently_played_tracks(self, limit=50):
        """Fetch the user's recently played tracks up to a limit."""
        try:
            results = self.spotify_client.current_user_recently_played(limit=limit)
            return results['items']
        except spotipy.SpotifyException as e:
            print(f"Spotify API Error: {str(e)}")
            return []
        except KeyError:
            print("Unexpected data format received from Spotify API.")
            return []

    def summarize_recent_plays(self, track_history):
        """Summarize recently played tracks into a more concise format."""
        track_summaries = []
        for item in track_history:
            played_at = item['played_at']
            track_name = item['track']['name']
            artist_names = ', '.join(artist['name'] for artist in item['track']['artists'])
            track_summaries.append({
                'played_at': played_at,
                'track_name': track_name,
                'artist_names': artist_names
            })
        return track_summaries

# Example usage:
# Assuming 'sp' is a properly authenticated Spotipy client instance using something like:
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope))
# history_data_instance = HistoryData(sp)
# recently_played = history_data_instance.get_recently_played_tracks(limit=20)
# track_summary = history_data_instance.summarize_recent_plays(recently_played)
# for track in track_summary:
#     print(f"{track['played_at']}: {track['track_name']} by {track['artist_names']}")