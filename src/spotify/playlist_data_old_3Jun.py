import spotipy

class PlaylistData:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client

    def get_user_playlists(self, limit=50, offset=0):
        return self.spotify_client.current_user_playlists(limit=limit, offset=offset)

    def get_playlist_tracks(self, playlist_id, limit=100, offset=0):
        return self.spotify_client.playlist_tracks(playlist_id, limit=limit, offset=offset)

    def get_playlist_details(self, playlist_id):
        return self.spotify_client.playlist(playlist_id)

# Example usage:
# Assuming 'sp' is an authenticated Spotipy client instance
# playlist_data_instance = PlaylistData(sp)
# user_playlists = playlist_data_instance.get_user_playlists(limit=20)
# playlist_tracks = playlist_data_instance.get_playlist_tracks(user_playlists['items'][0]['id'])
# playlist_details = playlist_data_instance.get_playlist_details(user_playlists['items'][0]['id'])