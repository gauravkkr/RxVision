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
import numpy as np

class OCRModel:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)
    def predict(self, image_path, threshold=0.25):
        img = cv2.imread(image_path)
        # Preprocessing: convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
        # Adaptive thresholding for binarization
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 31, 10)
        # Convert back to 3-channel for annotation
        proc_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        # OCR on preprocessed image
        text_ = self.reader.readtext(thresh)
        print(text_)
        for t_, t in enumerate(text_):
            bbox, text, score = t
            if score > threshold:
                pt1 = tuple(map(int, bbox[0]))  # top-left
                pt2 = tuple(map(int, bbox[2]))  # bottom-right
                cv2.rectangle(proc_img, pt1, pt2, (0, 255, 0), 2)
                cv2.putText(proc_img, text, pt1, cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
        return proc_img, text_
    
OCR_Model=OCRModel()

