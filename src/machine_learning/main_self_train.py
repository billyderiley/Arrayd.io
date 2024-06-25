import sys
sys.path.append(r'/workspaces/Arrayd.io')
import os
from src.data_processing.data_utils import load_data, create_dataloader, num_of_classes_from_unique_playlists
from model_training_self_train import self_training
from dotenv import load_dotenv

def main():
    """
    Main function to run the self-training process for semi-supervised learning.
    """
    load_dotenv()  # Ensure environment variables are loaded

    input_csv_path = os.getenv('AUDIO_ANALYSIS_INPUT_CSV_PATH')
    df = load_data(input_csv_path)
    num_classes, _ = num_of_classes_from_unique_playlists(df)

    print(f"Number of unique playlists: {num_classes}")

    # Split data into labeled and unlabeled datasets
    labeled_df = df.sample(frac=0.1, random_state=42)
    unlabeled_df = df.drop(labeled_df.index)

    labeled_dataloader, _, labeled_dataset = create_dataloader(labeled_df)
    unlabeled_dataloader, _, unlabeled_dataset = create_dataloader(unlabeled_df)

    # Infer the input size dynamically
    input_size = labeled_dataset.infer_input_size()
    print(f"Inferred input size: {input_size}")

    model = self_training(labeled_dataloader, unlabeled_dataloader, input_size, num_classes)
    print("\nTraining completed.")

if __name__ == "__main__":
    main()
