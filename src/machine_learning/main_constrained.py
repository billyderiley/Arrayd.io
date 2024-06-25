import sys
sys.path.append(r'/workspaces/Arrayd.io')
import os
import numpy as np
from src.data_processing.data_utils import load_data, create_dataloader, num_of_classes_from_unique_playlists
from model_training_constrained import constrained_clustering, create_pseudo_labeled_dataloader, train_model
from dotenv import load_dotenv

def extract_features_from_dataset(dataset):
    """
    Extract features from a dataset.
    
    Parameters:
    dataset (Dataset): PyTorch dataset
    
    Returns:
    numpy.ndarray: Extracted features
    """
    features = []
    for i in range(len(dataset)):
        feature, _ = dataset[i]
        features.append(feature.numpy())
    return np.array(features)

def create_constraints(df):
    """
    Create must-link and cannot-link constraints based on the existing playlists.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the data
    
    Returns:
    tuple: must_link and cannot_link constraints
    """
    must_link = []
    cannot_link = []
    playlist_dict = {'playlist1': [0, 1, 2], 'playlist2': [3, 4, 5]}  # Example playlists

    for playlist, tracks in playlist_dict.items():
        for i in range(len(tracks)):
            for j in range(i + 1, len(tracks)):
                must_link.append((tracks[i], tracks[j]))

    return np.array(must_link), np.array(cannot_link)

def main():
    """
    Main function to run the semi-supervised clustering process for creating playlists.
    """
    load_dotenv()  # Ensure environment variables are loaded

    input_csv_path = os.getenv('AUDIO_ANALYSIS_INPUT_CSV_PATH')
    df = load_data(input_csv_path)
    num_classes, _ = num_of_classes_from_unique_playlists(df)

    print(f"Number of unique playlists: {num_classes}")

    dataloader, _, dataset = create_dataloader(df)

    # Infer the input size dynamically
    input_size = dataset.infer_input_size()
    print(f"Inferred input size: {input_size}")

    # Extract features for clustering
    features = extract_features_from_dataset(dataset)

    # Create must-link and cannot-link constraints based on existing playlists
    must_link, cannot_link = create_constraints(df)

    num_clusters = num_classes  # Using the number of playlists as the number of clusters
    cluster_labels = constrained_clustering(features, must_link, cannot_link, num_clusters)

    # Create a DataLoader with pseudo-labeled data
    pseudo_labeled_dataloader = create_pseudo_labeled_dataloader(features, cluster_labels)

    # Train model with pseudo-labeled data
    model = train_model(pseudo_labeled_dataloader, input_size, num_clusters)
    print("\nTraining completed.")

if __name__ == "__main__":
    main()
