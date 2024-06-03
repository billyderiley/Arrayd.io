import pandas as pd
from playlist_data import PlaylistData

def create_tracks_dataframe(spotify_client):
    playlist_data = PlaylistData(spotify_client)
    user_playlists = playlist_data.get_user_playlists()

    total_playlists = len(user_playlists['items'])  # Total number of playlists to process

    # Initialize the DataFrame
    tracks_df = pd.DataFrame(columns=[
        'track_id', 'name', 'artists', 'album', 'duration_ms', 
        'explicit', 'popularity', 'preview_url', 'in_playlist_ids'
    ])

    # Iterate over user's playlists and their tracks
    #for playlist in user_playlists['items']:
    for index, playlist in enumerate(user_playlists['items'], start=1):
        playlist_id = playlist['id']
        playlist_tracks = playlist_data.get_playlist_tracks(playlist_id)

        # Print progress
        progress = (index / total_playlists) * 100  # Calculate progress as a percentage
        print(f"Loading... {progress:.2f}% completed", end='\r')

        # Add track data to the DataFrame
        for track_item in playlist_tracks['items']:
            track = track_item['track']
            track_id = track['id']
            track_details = {
                'track_id': track_id,
                'name': track['name'],
                'artists': '; '.join(artist['name'] for artist in track['artists']),
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'explicit': track['explicit'],
                'popularity': track['popularity'],
                'preview_url': track['preview_url'],
                'in_playlist_ids': playlist_id
            }

            # Using loc to assign data if the track_id already exists in the DataFrame
            if track_id in tracks_df['track_id'].values:
                tracks_df.loc[tracks_df['track_id'] == track_id, 'in_playlist_ids'] += f";{playlist_id}"
            else:
                # Using concat to add a new row to the DataFrame
                new_row = pd.DataFrame([track_details], columns=tracks_df.columns)
                tracks_df = pd.concat([tracks_df, new_row], ignore_index=True)


            # Append the track details to the DataFrame, handling tracks in multiple playlists
            #if track_id in tracks_df['track_id'].values:
            #    tracks_df.loc[tracks_df['track_id'] == track_id, 'in_playlist_ids'] += f";{playlist_id}"
            #else:
            #    tracks_df = tracks_df.append(track_details, ignore_index=True)
    print("\nFinished loading playlists.")  # New line after progress completion
    return tracks_df
