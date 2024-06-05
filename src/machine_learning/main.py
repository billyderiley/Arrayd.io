import sys
sys.path.append(r'/workspaces/Arrayd.io')

import os
from src.data_processing.download_previews import download_preview
from src.data_processing.audio_feature_extraction import extract_audio_features
from src.data_processing.data_utils import load_data, create_dataloader, num_of_classes_from_unique_playlists
from model_training import train_model
from dotenv import load_dotenv
import pandas as pd


def main():
    load_dotenv()  # Ensure environment variables are loaded

    input_csv_path = os.getenv('AUDIO_ANALYSIS_INPUT_CSV_PATH')
    df = load_data(input_csv_path)
    num_classes, all_playlists =  num_of_classes_from_unique_playlists(df)

    print(f"Number of unique playlists: {num_classes}")

    # Create a dictionary for playlist to index mapping
    playlist_to_idx = {playlist_id: idx for idx, playlist_id in enumerate(all_playlists)}

    dataloader, total_batches = create_dataloader(df, playlist_to_idx)
    
    # Correctly set input size based on your actual data processing
    input_size = 655360  # Updated based on actual feature size

    # Call train_model with the entire dataloader
    model = train_model(dataloader, input_size, num_classes)

    print("\nTraining completed.")

if __name__ == "__main__":
    main()
