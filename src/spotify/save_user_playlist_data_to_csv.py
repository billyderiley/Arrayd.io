import os

def save_dataframe_to_csv(dataframe, filename="users_tracks_and_playlists.csv"):
    # Construct the path dynamically using os.path.join for better cross-platform compatibility
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the directory of the script
    data_directory = os.path.join(base_dir, "spotify", "spotify_data")
    path = os.path.join(data_directory, filename)

    # Save the DataFrame to CSV
    print(f"Saving DataFrame to {path}...")
    dataframe.to_csv(path, index=False)
    print(f"DataFrame successfully saved to {path}")

"""def save_dataframe_to_csv(dataframe, filename="users_tracks_and_playlists.csv"):
    path = f"src/data/{filename}"
    print(f"Saving DataFrame to {path}...")
    dataframe.to_csv(path, index=False)
    print(f"DataFrame successfully saved to {path}")"""