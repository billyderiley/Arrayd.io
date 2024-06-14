import spotipy

class PlaylistData:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client

    def get_user_playlists(self, limit=None, offset=None):
        """Fetch user playlists with optional exclusion filters."""
        playlists = self.spotify_client.current_user_playlists(limit=limit, offset=offset)
        return playlists
    
    def filter_user_playlists(playlists, exclude_names=None, max_tracks=None):
        """Filter playlists based on the provided criteria"""
        filtered_playlists = []
        exclude_names = exclude_names or []

        for playlist in playlists['items']:
            # Check for name exclusions
            if any(exclude_name.lower() in playlist['name'].lower() for exclude_name in exclude_names):
                print("excluding ", playlist['name'])
                continue
            else:
                print("including ", playlist['name'])
            # Check for maximum track count
            if max_tracks is not None and playlist['tracks']['total'] > max_tracks:
                continue
            filtered_playlists.append(playlist)
        
        # Return the filtered playlists in the original format
        return {'items': filtered_playlists}

    def get_playlist_tracks(self, playlist_id, limit=None, offset=None):
        return self.spotify_client.playlist_tracks(playlist_id, limit=limit, offset=offset)

    def get_playlist_details(self, playlist_id):
        return self.spotify_client.playlist(playlist_id)
