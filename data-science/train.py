import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import cv2
from sklearn.model_selection import train_test_split

import pandas as pd
import cv2
from sklearn.model_selection import train_test_split

# Paths
DATASET_DIR = os.path.join('data', 'Doctors_Handwritten_Prescription_BD_dataset')
TRAIN_IMG_DIR = os.path.join(DATASET_DIR, 'Training', 'training_words')
TRAIN_LABELS = os.path.join(DATASET_DIR, 'Training', 'training_labels.csv')
VAL_IMG_DIR = os.path.join(DATASET_DIR, 'Validation', 'validation_words')
VAL_LABELS = os.path.join(DATASET_DIR, 'Validation', 'validation_labels.csv')


IMG_WIDTH = 128
IMG_HEIGHT = 32
BATCH_SIZE = 32
BATCH_SIZE = 32
# Increase epochs for better training
EPOCHS = 100

# 1. Load labels
train_df = pd.read_csv(TRAIN_LABELS)
val_df = pd.read_csv(VAL_LABELS)

# 2. Filter out missing files
train_df = train_df[train_df['IMAGE'].apply(lambda x: os.path.exists(os.path.join(TRAIN_IMG_DIR, x)))]
val_df = val_df[val_df['IMAGE'].apply(lambda x: os.path.exists(os.path.join(VAL_IMG_DIR, x)))]

# 3. Preprocess images and labels
import random
def preprocess_image(img_path, augment=False):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    # Data augmentation
    if augment:
        # Random rotation
        angle = random.uniform(-8, 8)
        M = cv2.getRotationMatrix2D((IMG_WIDTH/2, IMG_HEIGHT/2), angle, 1)
        img = cv2.warpAffine(img, M, (IMG_WIDTH, IMG_HEIGHT), borderMode=cv2.BORDER_REPLICATE)
        # Random noise
        if random.random() < 0.5:
            noise = np.random.normal(0, 0.05, img.shape)
            img = np.clip(img + noise*255, 0, 255)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=-1)
    return img

def load_data(df, img_dir, use_generic=False, augment=False):
    images = []
    labels = []
    label_col = 'GENERIC_NAME' if use_generic else 'MEDICINE_NAME'
    for _, row in df.iterrows():
        img_path = os.path.join(img_dir, row['IMAGE'])
        if os.path.exists(img_path):
            images.append(preprocess_image(img_path, augment=augment))
            labels.append(str(row[label_col]))
    return np.array(images), labels


# Set to True to use GENERIC_NAME as label
USE_GENERIC = False

print('Loading training data...')
X_train, y_train = load_data(train_df, TRAIN_IMG_DIR, use_generic=USE_GENERIC, augment=True)
print('Loading validation data...')
X_val, y_val = load_data(val_df, VAL_IMG_DIR, use_generic=USE_GENERIC, augment=False)


# 4. Build character vocabulary
all_text = ''.join(y_train + y_val)
vocab = sorted(set(all_text))
char_to_num = keras.layers.StringLookup(vocabulary=list(vocab), oov_token="")
num_to_char = keras.layers.StringLookup(vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True)

max_label_len = max([len(label) for label in y_train + y_val])

# 5. Encode labels for CTC
def encode_labels(labels):
    label_seqs = []
    for label in labels:
        label_seq = char_to_num(tf.strings.unicode_split(label, input_encoding="UTF-8"))
        label_seqs.append(label_seq.numpy())
    label_seqs = keras.preprocessing.sequence.pad_sequences(label_seqs, maxlen=max_label_len, padding='post')
    return np.array(label_seqs)

y_train_enc = encode_labels(y_train)
y_val_enc = encode_labels(y_val)

# 6. Model (CNN + CTC)
def build_model():
    input_img = layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1), name='image')
    labels = layers.Input(name="label", shape=(max_label_len,), dtype="float32")
    x = layers.Conv2D(32, (3,3), activation='relu', padding='same')(input_img)
    x = layers.MaxPooling2D((2,2))(x)
    x = layers.Conv2D(64, (3,3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2,2))(x)
    new_shape = ((IMG_WIDTH // 4), (IMG_HEIGHT // 4) * 64)
    x = layers.Reshape(target_shape=new_shape)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)
    x = layers.Dense(len(char_to_num.get_vocabulary()) + 1, activation="softmax", name="output")(x)
    # CTC loss as a Lambda layer
    def ctc_lambda_func(args):
        y_pred, labels = args
        input_length = tf.ones(shape=(tf.shape(y_pred)[0], 1), dtype=tf.float32) * tf.cast(tf.shape(y_pred)[1], tf.float32)
        label_length = tf.ones(shape=(tf.shape(labels)[0], 1), dtype=tf.float32) * tf.cast(tf.shape(labels)[1], tf.float32)
        return keras.backend.ctc_batch_cost(labels, y_pred, input_length, label_length)
    loss_out = layers.Lambda(ctc_lambda_func, output_shape=(1,), name='ctc')([x, labels])
    model = keras.Model(inputs=[input_img, labels], outputs=loss_out)
    return model

model = build_model()
model.compile(optimizer='adam', loss={'ctc': lambda y_true, y_pred: y_pred})


print(model.summary())

# 7. Real CTC training loop
print('Training (CTC)...')
train_inputs = {
    'image': X_train,
    'label': y_train_enc
}
val_inputs = {
    'image': X_val,
    'label': y_val_enc
}
dummy_y = np.zeros((len(X_train), 1))
dummy_y_val = np.zeros((len(X_val), 1))
model.fit(train_inputs, dummy_y, validation_data=(val_inputs, dummy_y_val), epochs=EPOCHS, batch_size=BATCH_SIZE)

print('Training complete! For decoding predictions, use CTC decoding with num_to_char.')

def load_data(data_dir, img_size=(28, 28)):
    # Placeholder: expects data_dir/class_name/image.png structure
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0)
    train_gen = datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        color_mode='grayscale',
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    val_gen = datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        color_mode='grayscale',
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )
    return train_gen, val_gen

def build_model(num_classes, img_size=(28, 28)):
    model = keras.Sequential([
        layers.Input(shape=img_size + (1,)),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def main():
    data_dir = 'data'  # Place your handwriting dataset here
    img_size = (28, 28)

