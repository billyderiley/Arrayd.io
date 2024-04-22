def save_dataframe_to_csv(dataframe, filename="users_tracks_and_playlists.csv"):
    path = f"src/data/{filename}"
    print(f"Saving DataFrame to {path}...")
    dataframe.to_csv(path, index=False)
    print(f"DataFrame successfully saved to {path}")