import ast
import numpy as np
import matplotlib.pyplot as plt

def plot_mel_spectrogram(track_id, feature_data, title=None):
    # Handle the feature_data format: assume it's a single string of space-separated floats wrapped in brackets
    if feature_data.startswith('[') and feature_data.endswith(']'):
        # Remove the brackets and split by spaces
        feature_data = feature_data[1:-1].split()  # this might need adjustment if data includes line breaks or other characters
        feature_data = np.array([float(num) for num in feature_data])  # convert strings to floats

    # Check the shape of feature_data and reshape if necessary
    feature_length = int(np.sqrt(len(feature_data)))  # Assuming the feature is a square matrix
    if feature_length ** 2 == len(feature_data):  # Check if it can form a square matrix
        feature_data = feature_data.reshape((feature_length, feature_length))

    plt.figure(figsize=(10, 4))
    plt.imshow(feature_data, aspect='auto', origin='lower', cmap='viridis')
    plt.title(title or f'Mel Spectrogram for Track ID {track_id}')
    plt.xlabel('Time')
    plt.ylabel('Mel Frequency Bin')
    plt.colorbar(label='Amplitude (dB)')
    plt.show()

# Example usage
if __name__ == "__main__":
    # This example usage block is for demonstration.
    # You would normally call this function with data retrieved using the load_features script.
    plot_mel_spectrogram('track_id123', '[[0, 1, 2], [3, 4, 5]]', 'Example Mel Spectrogram')
