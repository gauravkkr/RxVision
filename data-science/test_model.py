import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2

# --- Copy your vocab and num_to_char setup from train.py ---
# Example (replace with your actual vocab):
# vocab = [...]
# num_to_char = keras.layers.StringLookup(vocabulary=vocab, oov_token="", invert=True)

# For demonstration, we will reload vocab from training data
import pandas as pd
DATASET_DIR = os.path.join('data', 'Doctors_Handwritten_Prescription_BD_dataset')
TRAIN_LABELS = os.path.join(DATASET_DIR, 'Training', 'training_labels.csv')
VAL_LABELS = os.path.join(DATASET_DIR, 'Validation', 'validation_labels.csv')
train_df = pd.read_csv(TRAIN_LABELS)
val_df = pd.read_csv(VAL_LABELS)
y_train = [str(row['MEDICINE_NAME']) for _, row in train_df.iterrows()]
y_val = [str(row['MEDICINE_NAME']) for _, row in val_df.iterrows()]
all_text = ''.join(y_train + y_val)
vocab = sorted(set(all_text))
num_to_char = keras.layers.StringLookup(vocabulary=list(vocab), oov_token="", invert=True)

# --- Load model ---
model = keras.models.load_model('handwriting_model.h5', compile=False)

# --- Preprocess test image ---
def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 32))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=-1)
    return np.expand_dims(img, axis=0)  # Add batch dimension

# --- Set your test image path here ---
img_path = 'data/Doctors_Handwritten_Prescription_BD_dataset/Testing/testing_words/0.png'  # Change to your image
img = preprocess_image(img_path)

# --- Predict ---
y_pred = model.predict(img)
input_len = np.ones(y_pred.shape[0]) * y_pred.shape[1]
results = keras.backend.ctc_decode(y_pred, input_length=input_len, greedy=True)[0][0].numpy()

# --- Decode to string ---
output_text = ''.join([num_to_char(x).numpy().decode('utf-8') for x in results[0] if x != 0])
print('Predicted text:', output_text)
