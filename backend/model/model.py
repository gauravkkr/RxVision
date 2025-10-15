import cv2
import easyocr
import numpy as np
import string


def _normalize_text(s: str) -> str:
    s = s.lower()
    # remove punctuation and extra whitespace
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = ' '.join(s.split())
    return s


class OCRModel:
    """Improved OCR model wrapper that runs multiple preprocessing passes
    and aggregates results to increase text-extraction accuracy.
    """

    def __init__(self, languages=None, gpu=False):
        langs = languages or ['en']
        # easyocr.Reader initialization can be slow; keep a single reader
        self.reader = easyocr.Reader(langs, gpu=gpu)

    def _clahe(self, gray):
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(gray)

    def _adaptive_thresh(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 31, 10)
        return thresh

    def _binarize_otsu(self, gray):
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return otsu

    def predict(self, image_path, threshold=0.2, debug=False):
        """Run multiple OCR passes on different preprocessed variants and
        aggregate results.

        Returns:
            annotated_img: image with boxes drawn
            aggregated: list of (bbox, text, score)
        """
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        h, w = img.shape[:2]

        # prepare variants: original, clahe, adaptive thresh, scaled
        variants = []
        variants.append(('orig', img))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = self._clahe(gray)
        variants.append(('clahe', cv2.cvtColor(clahe, cv2.COLOR_GRAY2BGR)))

        adaptive = self._adaptive_thresh(img)
        variants.append(('adaptive', cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)))

        otsu = self._binarize_otsu(gray)
        variants.append(('otsu', cv2.cvtColor(otsu, cv2.COLOR_GRAY2BGR)))

        # scaled-up variant (helpful for small text)
        scale = 2.0
        big = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        variants.append(('scale2', big))

        raw_results = []

        for name, var in variants:
            # easyocr works with grayscale or color, keep grayscale for binarized variants
            try:
                if len(var.shape) == 2:
                    res = self.reader.readtext(var)
                else:
                    res = self.reader.readtext(var)
            except Exception as e:
                if debug:
                    print(f"OCR pass '{name}' failed: {e}")
                res = []

            for bbox, text, score in res:
                # bbox may be for a scaled image; normalize coordinates to original image size
                if name == 'scale2':
                    # scale down bbox coordinates
                    scaled_bbox = [[pt[0] / scale, pt[1] / scale] for pt in bbox]
                    norm_bbox = scaled_bbox
                else:
                    norm_bbox = bbox

                raw_results.append({'bbox': norm_bbox, 'text': text, 'score': float(score)})

        # Aggregate by normalized text, keep highest score per normalized string
        aggregated_map = {}
        for r in raw_results:
            norm = _normalize_text(r['text'])
            if not norm:
                continue
            if norm not in aggregated_map or r['score'] > aggregated_map[norm]['score']:
                aggregated_map[norm] = r

        # Convert aggregated_map to list and filter by threshold
        aggregated = []
        for norm, entry in aggregated_map.items():
            if entry['score'] >= threshold:
                aggregated.append((entry['bbox'], entry['text'], entry['score']))

        # Sort by score desc
        aggregated.sort(key=lambda x: x[2], reverse=True)

        # Annotate image (draw boxes on a copy of original)
        annotated = img.copy()
        for bbox, text, score in aggregated:
            try:
                pt1 = tuple(map(int, bbox[0]))
                pt2 = tuple(map(int, bbox[2]))
            except Exception:
                # fallback: compute bounding rect from points
                pts = np.array(bbox, dtype=np.int32)
                x, y, w_box, h_box = cv2.boundingRect(pts)
                pt1 = (x, y)
                pt2 = (x + w_box, y + h_box)

            cv2.rectangle(annotated, pt1, pt2, (0, 255, 0), 2)
            cv2.putText(annotated, text, (pt1[0], max(pt1[1] - 6, 0)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return annotated, aggregated


OCR_Model = OCRModel()

