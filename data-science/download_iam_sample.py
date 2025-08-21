# Download and prepare the IAM Handwriting Database (sample)
# This script will download a small sample of the IAM dataset and prepare it for training.
# For full dataset, you need to register at https://fki.tic.heia-fr.ch/databases/iam-handwriting-database and download manually.

import os
import urllib.request
import zipfile

DATA_DIR = 'data/iam_sample'
ZIP_URL = 'https://github.com/githubharald/SimpleHTR/releases/download/0.1/word_sample.zip'
ZIP_PATH = os.path.join(DATA_DIR, 'word_sample.zip')

os.makedirs(DATA_DIR, exist_ok=True)

print('Downloading sample dataset...')
urllib.request.urlretrieve(ZIP_URL, ZIP_PATH)

print('Extracting...')
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR)

print('Done! Sample IAM handwriting data is ready in', DATA_DIR)
