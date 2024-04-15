import xml.etree.ElementTree as ET
import os

itunes_library_path = os.getenv('ITUNES_LIBRARY_PATH')
if itunes_library_path is None:
    raise ValueError("Please set the ITUNES_LIBRARY_PATH environment variable.")


# Function to parse the XML and extract playlists
def parse_itunes_library(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    playlists = []

    for node in root.findall('dict/dict/dict'):
        playlist = {}
        playlist_songs = []
        playlist_name = None
        parsing_songs = False

        for child in node:
            if child.tag == 'key':
                if child.text == 'Name':
                    parsing_songs = False
                elif child.text == 'Playlist Items':
                    parsing_songs = True
            elif child.tag == 'string' and not parsing_songs:
                playlist_name = child.text
            elif child.tag == 'array' and parsing_songs:
                for song in child.findall('dict'):
                    song_id = song.find('integer').text
                    playlist_songs.append(song_id)

        if playlist_name:
            playlist['name'] = playlist_name
            playlist['songs'] = playlist_songs
            playlists.append(playlist)

    return playlists


# Example usage
playlists = parse_itunes_library(itunes_library_path)
for playlist in playlists:
    print(f"Playlist: {playlist['name']}, Songs: {playlist['songs']}")
