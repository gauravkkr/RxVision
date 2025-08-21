import keras_ocr
import matplotlib.pyplot as plt

# Create a pre-trained OCR pipeline
pipeline = keras_ocr.pipeline.Pipeline()

# Path to your test image (change as needed)
image_path = 'data/Doctors_Handwritten_Prescription_BD_dataset/Testing/testing_words/0.png'
image = keras_ocr.tools.read(image_path)

# Run OCR
prediction_groups = pipeline.recognize([image])

# Print detected text
print('Detected words:')
for text, box in prediction_groups[0]:
    print(text)

# Optional: visualize results
keras_ocr.tools.drawAnnotations(image, prediction_groups[0])
plt.imshow(image)
plt.axis('off')
plt.show()
