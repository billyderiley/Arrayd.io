import spotipy

class PlaylistData:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client

    def get_user_playlists(self, limit=50, offset=0, exclude_names=None, max_tracks=None):
        """Fetch user playlists with optional exclusion filters."""
        playlists = self.spotify_client.current_user_playlists(limit=limit, offset=offset)
        filtered_playlists = []
        exclude_names = exclude_names or []
        
        # Filter playlists based on the provided criteria
        for playlist in playlists['items']:
            # Check for name exclusions
            if any(exclude_name.lower() in playlist['name'].lower() for exclude_name in exclude_names):
                continue
            # Check for maximum track count
            if max_tracks is not None and playlist['tracks']['total'] > max_tracks:
                continue
            filtered_playlists.append(playlist)
        
        # Return the filtered playlists in the original format
        return {'items': filtered_playlists}

    def get_playlist_tracks(self, playlist_id, limit=100, offset=0):
        return self.spotify_client.playlist_tracks(playlist_id, limit=limit, offset=offset)

    def get_playlist_details(self, playlist_id):
        return self.spotify_client.playlist(playlist_id)
