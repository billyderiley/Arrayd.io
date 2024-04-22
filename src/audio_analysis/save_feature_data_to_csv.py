import pandas as pd

def save_feature_data_to_csv(feature_data, output_csv_path='data/feature_data.csv'):
    # Save the feature data to CSV
    feature_data.to_csv(output_csv_path, index=False)
    print(f"Feature data successfully saved to {output_csv_path}")
