import spotipy

class UserData:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client

    def get_user_profile(self):
        return self.spotify_client.current_user()

    def get_user_saved_tracks(self, limit=50, offset=0):
        return self.spotify_client.current_user_saved_tracks(limit=limit, offset=offset)

    def get_user_top_artists_and_tracks(self, limit=20, time_range='medium_term'):
        top_artists = self.spotify_client.current_user_top_artists(limit=limit, time_range=time_range)
        top_tracks = self.spotify_client.current_user_top_tracks(limit=limit, time_range=time_range)
        return top_artists, top_tracks

# Example usage:
# Assuming 'sp' is an authenticated Spotipy client instance
# user_data_instance = UserData(sp)
# user_profile = user_data_instance.get_user_profile()
# user_saved_tracks = user_data_instance.get_user_saved_tracks(limit=20)
# user_top_artists, user_top_tracks = user_data_instance.get_user_top_artists_and_tracks(limit=10, time_range='short_term')