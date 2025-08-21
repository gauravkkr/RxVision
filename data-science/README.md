# Data Science for RXvision

This folder contains scripts and notebooks for training models to recognize both handwritten and printed text.

## Structure
- `models/` — Trained model files will be saved here.
- `notebooks/` — Jupyter notebooks for experiments and training.
- `train.py` — Main script to train a handwriting recognition model.
- `requirements.txt` — Python dependencies for training.

## Getting Started
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run training:
   ```
   python train.py
   ```

## Note
- You will need a dataset of handwritten images and their labels (e.g., IAM, EMNIST, or your own scanned notes).
- The provided script is a template. For best results, use a large, diverse handwriting dataset.