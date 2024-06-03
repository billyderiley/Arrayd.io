from populate_feature_data import populate_feature_data
from dotenv import load_dotenv
import os

def main():
    # Call the function to populate feature data
    csv_path = os.getenv('AUDIO_ANALYSIS_INPUT_CSV_PATH')
    output_csv_path = os.getenv('AUDIO_ANALYSIS_OUTPUT_CSV_PATH')
    batch_size = int(os.getenv('AUDIO_ANALYSIS_BATCH_SIZE'))
    populate_feature_data(csv_path=csv_path, output_csv_path=output_csv_path, batch_size=batch_size)

if __name__ == '__main__':
    main()