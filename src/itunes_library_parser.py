import xml.etree.ElementTree as ET
import os
import configparser
print("hey")
# Initialize the ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file by providing the relative path
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
config.read(config_path)

# Get the iTunes Library path
itunes_library_path = config.get('Paths', 'ItunesLibraryPath', fallback=None)

if itunes_library_path is None:
    raise ValueError("The iTunesLibraryPath is not set in the config.ini file.")

# Function to parse the XML and extract tracks and playlists
def parse_itunes_library(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Assuming the first 'dict' under the root is the main dictionary
    main_dict = root.find('dict')

    # Initialize empty dictionaries for tracks and playlists
    tracks = {}
    playlists = []

    # Iterate over the elements in the main dictionary
    iter_main_dict = iter(main_dict)
    for elem in iter_main_dict:
        if elem.tag == 'key' and elem.text == 'Tracks':
            # The next element after the key 'Tracks' is the dictionary containing tracks
            tracks_dict = next(iter_main_dict)
            for dict_elem in tracks_dict.findall('dict'):
                # Extract track ID and details here
                track_id = dict_elem.find('key').text
                name = dict_elem.find('string').text  # This might need to be adjusted depending on the structure
                tracks[track_id] = name

        elif elem.tag == 'key' and elem.text == 'Playlists':
            # The next element after the key 'Playlists' is the array containing playlists
            playlists_array = next(iter_main_dict)
            for plist in playlists_array.findall('dict'):
                # Extract playlist details here
                playlist_info = {'name': None, 'tracks': []}
                playlist_items = plist.findall('array')[0] if plist.findall('array') else None
                if playlist_items is not None:
                    for track_dict in playlist_items.findall('dict'):
                        track_id_elem = track_dict.find('integer')
                        if track_id_elem is not None and track_id_elem.text in tracks:
                            playlist_info['tracks'].append(tracks[track_id_elem.text])
                playlists.append(playlist_info)

    return playlists

# Example usage
playlists = parse_itunes_library(itunes_library_path)
for playlist in playlists:
    print(f"Playlist: {playlist['name']}")
    for track in playlist['tracks']:
        print(f"    Track: {track}")