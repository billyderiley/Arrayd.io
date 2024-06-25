import sys
sys.path.append(r'/workspaces/Arrayd.io')

import pandas as pd
from playlist_data import PlaylistData
from spotify_utils import check_download_duration
from src.data_processing.download_previews import download_preview

from src.storage_access.sql_utils import update_database
from src.storage_access.file_storage import store_download

#def create_tracks_dataframe(spotify_client, limit, store_entries=True, include_no_preview=False, exclude_names=None, max_tracks=None):
def create_tracks_dataframe(user_playlists, spotify_client, store_entries=True, include_no_preview=False):
    #playlist_data = PlaylistData(spotify_client)
    #user_playlists = playlist_data.get_user_playlists(limit, exclude_names=exclude_names, max_tracks=max_tracks)


    #total_playlists = len(user_playlists['items'])  # Total number of playlists to process
    total_playlists = len(user_playlists)  # Total number of playlists to process

    # Initialize the DataFrame
    tracks_df = pd.DataFrame(columns=[
        'track_id', 'name', 'artists', 'album', 'duration_ms', 
        'explicit', 'popularity', 'preview_url', 'in_playlist_ids'
    ])

    # Iterate over user's playlists and their tracks
    #for index, playlist in enumerate(user_playlists['items'], start=1):
    for index, playlist in enumerate(user_playlists, start=1):
        playlist_id = playlist['id']
        playlist_tracks = PlaylistData(spotify_client).get_playlist_tracks(playlist_id)

        # Print progress
        progress = (index / total_playlists) * 100  # Calculate progress as a percentage
        print(f"Loading... {progress:.2f}% completed", end='\r')

        # Add track data to the DataFrame
        for track_item in playlist_tracks['items']:
            track = track_item['track']
            track_id = track['id']
            if track['preview_url'] or include_no_preview:  # Check if preview_url exists or include tracks without preview
                audio_buffer, error = download_preview(track_id, track['preview_url'])
                duration = check_download_duration(audio_buffer)
                if duration != 29.71265306122449:
                    print("duration is not the accepted nuber, skipping. Duration : ", duration, " ID : ", track_id)
                    continue
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

                # Append the track details to the DataFrame
                if track_id in tracks_df['track_id'].values:
                    tracks_df.loc[tracks_df['track_id'] == track_id, 'in_playlist_ids'] += f";{playlist_id}"
                else:
                    new_row = pd.DataFrame([track_details], columns=tracks_df.columns)
                    tracks_df = pd.concat([tracks_df, new_row], ignore_index=True)
                    if store_entries is True:
                        file_path = store_download(audio_buffer, track_id)
                        update_database(track_id, file_path)

    print("\nFinished loading playlists.")  # New line after progress completion
    return tracks_df
