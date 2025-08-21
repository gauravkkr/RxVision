from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load processor and model
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-small-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-small-handwritten')

# Path to your test image (change as needed)
image_path = 'data/Doctors_Handwritten_Prescription_BD_dataset/Testing/testing_words/0.png'
image = Image.open(image_path).convert('RGB')

# Preprocess and predict
pixel_values = processor(images=image, return_tensors="pt").pixel_values
with torch.no_grad():
    generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print('Predicted text:', generated_text)
