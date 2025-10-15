

from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename

import os
import cv2
import sys
import json
import logging
from rapidfuzz import process as fuzzy_process
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model import OCR_Model
from model.medicine_list_auto import MEDICINE_LIST, MEDICINE_ALIAS_MAP

api_bp = Blueprint('api', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../static/uploads/')
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), '../static/results/')






def process_image(file):
    filename = secure_filename(file.filename)
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(img_path)

    # Call the OCR model to process the image
    annotated_image, text_output = OCR_Model.predict(img_path)

    # Save the annotated image
    annotated_image_filename = 'annotated_' + filename
    annotated_image_path = os.path.join(RESULTS_FOLDER, annotated_image_filename)
    cv2.imwrite(annotated_image_path, annotated_image)

    # text_output is now a list of (bbox, text, score)
    extracted_text = []
    for item in text_output:
        if len(item) >= 2:
            extracted_text.append(item[1])
    
    # Save the extracted text to a results file
    result_txt_path = os.path.join(RESULTS_FOLDER, 'result.txt')
    with open(result_txt_path, 'w', encoding='utf-8') as result_file:
        result_file.write("\n".join(extracted_text))
    
    # Fuzzy match each extracted text line to medicine names
    print("[DEBUG] Extracted text:", extracted_text)
    guessed_medicines = []
    from rapidfuzz import process as fuzzy_process
    from rapidfuzz import fuzz

    # helper: try direct alias mapping first
    alias_map = MEDICINE_ALIAS_MAP if 'MEDICINE_ALIAS_MAP' in globals() else {}

    for line in extracted_text:
        raw = line or ''
        clean_line = raw.lower().strip()
        if len(clean_line) < 2:
            continue

        # check alias map exact
        if clean_line in alias_map:
            guess = alias_map[clean_line]
            guessed_medicines.append({'input': raw, 'guess': guess, 'score': 100, 'method': 'Alias'})
            continue

        # 1) exact or substring match (fast)
        substring_matches = [m for m in MEDICINE_LIST if clean_line in m.lower() or m.lower() in clean_line]
        if substring_matches:
            guessed_medicines.append({'input': raw, 'guess': substring_matches[0], 'score': 95, 'method': 'Substring'})
            continue

        # 2) partial ratio across list, keep threshold lower for short strings
        best_match = None
        best_score = 0
        score_threshold = 60 if len(clean_line) >= 5 else 45
        for med in MEDICINE_LIST:
            score = fuzz.partial_ratio(clean_line, med.lower())
            if score > best_score:
                best_score = score
                best_match = med

        if best_score >= score_threshold:
            print(f"[DEBUG] Partial fuzzy matched '{raw}' to '{best_match}' with score {best_score}")
            guessed_medicines.append({'input': raw, 'guess': best_match, 'score': best_score, 'method': 'Partial Fuzzy'})
            continue

        # 3) fallback to full fuzzy extractOne
        result = fuzzy_process.extractOne(clean_line, MEDICINE_LIST, score_cutoff=40)
        if result:
            match, score, _ = result
            print(f"[DEBUG] Fuzzy matched '{raw}' to '{match}' with score {score}")
            guessed_medicines.append({'input': raw, 'guess': match, 'score': score, 'method': 'Fuzzy'})
        else:
            print(f"[DEBUG] No fuzzy match found for '{raw}'")

    return jsonify({
        'text': extracted_text,
        'annotated_image': annotated_image_filename,
        'guessed_medicines': guessed_medicines
    })

@api_bp.route('/imageupload', methods=['POST'])
def image_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'no selected file'}), 400
    
    if file:
        return process_image(file)
    
    return jsonify({'error': 'file processing failed'}), 500

@api_bp.route('/test', methods=['GET'])
def test_route():
    return "Test route is working!"

@api_bp.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle(path):
    """
    Handle all other API routes.
    This function will be called for any API route that doesn't match a specific route above.
    """
    # Log the incoming request for debugging
    logging.debug(f"Handling API request for path: {path}")
    logging.debug(f"Request method: {request.method}")
    logging.debug(f"Request data: {request.get_json(silent=True)}")

    # Here you can add logic to route to different functions based on the path
    # if path == 'some/specific/path':
    #     # Handle a specific path
    #     return jsonify({"message": f"Handled specific path: {path}"})
    
    # If no specific handling, return a generic response
    return jsonify({"message": f"Received request for unhandled API path: {path}"}), 404

# Error handling
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500