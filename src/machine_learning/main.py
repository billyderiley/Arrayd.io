import sys
sys.path.append(r'/workspaces/Arrayd.io')
import os
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

    dataloader, total_batches, dataset = create_dataloader(df)

    # Infer the input size dynamically
    input_size = dataset.infer_input_size()
    print(f"Inferred input size: {input_size}")

    model = train_model(dataloader, input_size, num_classes)
    print("\nTraining completed.")

if __name__ == "__main__":
    main()
