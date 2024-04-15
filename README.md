# Arrayd.io
A Python app for analyzing and learning the vibe of music playlists

## Project Structure

This project is organized as follows:

- `data/`: Contains sample datasets and data-related scripts. Real data is not tracked due to privacy concerns.
- `docs/`: Documentation on installation, usage, and contribution guidelines.
- `notebooks/`: Jupyter notebooks for demonstrations and experiments.
- `src/`: Source code including the main application logic.
    - `itunes_library_parser.py`: Parses the iTunes/Music XML.
    - `model.py`: The deep learning model.
    - `prepare_data.py`: Prepares the dataset for the model.
    - `torch_audio_feature_extraction.py`: Audio feature extraction.
- `tests/`: Unit tests for the application code.
- `README.md`: The guide to this project, how to install and run it.
- `.gitignore`: Specifies untracked files that Git should ignore.
- `setup_project.sh`: Script to set up the project environment (optional).

Each directory contains a README.md file that further explains the contents
