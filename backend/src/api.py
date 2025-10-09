

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
    import google.generativeai as genai
    import PIL.Image
    # Configure Gemini API (move to top-level in production)
    genai.configure(api_key="AIzaSyAy6PzooCbZF4ey-Ufa25Tg_YyKN_-9nSE")

    filename = secure_filename(file.filename)
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(img_path)

    image = PIL.Image.open(img_path)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [
            "You are a medical OCR assistant. "
            "Analyze the provided image for any text, focusing specifically on handwritten or printed medicine names. "
            "Strictly cross-reference the recognized text against a comprehensive, real-world medicine database."
            "If a clear match is found, output the confirmed medicine name."
            "If the handwriting is ambiguous, use your deep medical knowledge to infer the most likely valid medicine name from the context and letter shapes. Do not guess or hallucinate a non-existent word."
            "If the handwriting is ambiguous, prioritize the most common letters and letter combinations in medical terminology. For example, 'rine' is a more common ending than 'xim' in a medicine name."
            "Output ONLY the valid medicine name from real-world medicines (e.g., Paracetamol, Ibuprofen, Amoxicillin, etc.). "
            "If handwriting is unclear, give the closest valid medicine name, not a made-up word. "
            "Do not output anything except the medicine name.",
            image
        ],
        generation_config={"temperature": 0.0}
    )

    medicines = []
    if response and hasattr(response, "text"):
        medicines = [line.strip() for line in response.text.split("\n") if line.strip()]

    # Save the image as annotated (for UI compatibility)
    annotated_image_filename = filename
    annotated_image_path = os.path.join(RESULTS_FOLDER, annotated_image_filename)
    image.save(annotated_image_path)

    return jsonify({
        'text': medicines,
        'annotated_image': annotated_image_filename,
        'guessed_medicines': [{'input': m, 'guess': m, 'score': 100, 'method': 'Gemini'} for m in medicines]
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