import cv2
import easyocr
import numpy as np

class OCRModel:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)
    def predict(self,image_path,threshold=0.25):
        img=cv2.imread(image_path)
        text_ = self.reader.readtext(img)
        print(text_)
        for t_, t in enumerate(text_):
            bbox, text, score = t
            if score > threshold:
                cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
                cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
        return img, text_
    
OCR_Model=OCRModel()

