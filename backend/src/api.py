

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
    extracted_text = [t[1] for t in text_output]
    
    # Save the extracted text to a results file
    result_txt_path = os.path.join(RESULTS_FOLDER, 'result.txt')
    with open(result_txt_path, 'w') as result_file:
        result_file.write("\n".join(extracted_text))
    
    # Fuzzy match each extracted text line to medicine names


    # Simple substring match: for each extracted line, find first medicine name containing at least 3 consecutive letters from the line
    print("[DEBUG] Extracted text:", extracted_text)
    guessed_medicines = []
    from rapidfuzz import process as fuzzy_process
    for line in extracted_text:
        clean_line = line.lower().strip()
        
        # Skip very short lines (less than 2 characters)
        if len(clean_line) < 2:
            continue
            
        # Try direct prefix match (prioritize 2-letter for better OCR matching)
        prefix2 = clean_line[:2]
        prefix3 = clean_line[:3] if len(clean_line) >= 3 else clean_line
        direct_match = None
        
        # First try 2-letter prefix (more reliable for partial OCR)
        for med in MEDICINE_LIST:
            med_lower = med.lower()
            if med_lower.startswith(prefix2):
                direct_match = med
                print(f"[DEBUG] Direct prefix matched '{line}' to '{med}' (2-letter)")
                guessed_medicines.append({'input': line, 'guess': med, 'score': 100, 'method': 'Direct prefix (2-letter)'})
                break
        
        # If no 2-letter match and we have 3+ characters, try 3-letter prefix
        if not direct_match and len(clean_line) >= 3:
            for med in MEDICINE_LIST:
                med_lower = med.lower()
                if med_lower.startswith(prefix3):
                    direct_match = med
                    print(f"[DEBUG] Direct prefix matched '{line}' to '{med}' (3-letter)")
                    guessed_medicines.append({'input': line, 'guess': med, 'score': 100, 'method': 'Direct prefix (3-letter)'})
                    break
                
        if not direct_match:
            # Try fuzzy matching with partial ratio for better OCR text recognition
            from rapidfuzz import fuzz
            best_match = None
            best_score = 0
            for med in MEDICINE_LIST:
                # Use partial ratio which is better for partial text matches
                score = fuzz.partial_ratio(clean_line, med.lower())
                if score > best_score and score >= 60:  # Lower threshold for partial matches
                    best_score = score
                    best_match = med
            
            if best_match:
                print(f"[DEBUG] Partial fuzzy matched '{line}' to '{best_match}' with score {best_score}")
                guessed_medicines.append({'input': line, 'guess': best_match, 'score': best_score, 'method': 'Partial Fuzzy'})
            else:
                # Fallback to regular fuzzy matching
                result = fuzzy_process.extractOne(clean_line, MEDICINE_LIST, score_cutoff=40)
                if result:
                    match, score, _ = result
                    print(f"[DEBUG] Fuzzy matched '{line}' to '{match}' with score {score}")
                    guessed_medicines.append({'input': line, 'guess': match, 'score': score, 'method': 'Fuzzy'})
                else:
                    print(f"[DEBUG] No fuzzy match found for '{line}'")

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