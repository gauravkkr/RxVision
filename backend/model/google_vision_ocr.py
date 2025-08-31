import os
from google.cloud import vision
from google.oauth2 import service_account
import cv2
import numpy as np

class GoogleVisionOCR:
    def __init__(self, credentials_path=None):
        if credentials_path is None:
            credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError('Google Vision API credentials not found.')
        self.client = vision.ImageAnnotatorClient(credentials=service_account.Credentials.from_service_account_file(credentials_path))

    def predict(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = self.client.document_text_detection(image=image)
        if response.error.message:
            raise Exception(f'Google Vision API error: {response.error.message}')
        # Extract text
        text = response.full_text_annotation.text
        # Optionally, draw bounding boxes on the image
        img = cv2.imread(image_path)
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        vertices = [(v.x, v.y) for v in word.bounding_box.vertices]
                        if len(vertices) == 4:
                            cv2.rectangle(img, vertices[0], vertices[2], (0,255,0), 2)
        return img, text
