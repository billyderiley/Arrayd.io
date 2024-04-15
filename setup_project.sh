#!/bin/bash

# Define the base directory
BASE_DIR="Arrayd.io"

# Create directories
mkdir -p $BASE_DIR/src $BASE_DIR/data $BASE_DIR/docs $BASE_DIR/tests $BASE_DIR/notebooks

# Create files in src
touch $BASE_DIR/src/itunes_library_parser.py
touch $BASE_DIR/src/torch_audio_feature_extraction.py
touch $BASE_DIR/src/prepare_data.py
touch $BASE_DIR/src/model.py

# Create files in data
echo "# Data Directory
This directory contains data used for the Arrayd.io project. Note that due to privacy concerns and GitHub size limitations, actual audio files and detailed user data are not included in this repository.

## Structure
- playlists.xml: Example XML file containing playlist data exported from the iTunes/Music app." > $BASE_DIR/data/README.md

# Create documentation files
echo "# Installation Guide

## Requirements
- Python 3.8+
- PyTorch, TorchAudio

## Setup
Clone this repository and install required packages:

```bash
git clone https://github.com/YOUR_USERNAME/Arrayd.io.git
cd Arrayd.io
pip install -r requirements.txt
```" > $BASE_DIR/docs/installation.md

echo "# Usage Guide

## Parsing iTunes Library
Run the itunes_library_parser.py to parse your iTunes/Music XML:

```bash
python src/itunes_library_parser.py