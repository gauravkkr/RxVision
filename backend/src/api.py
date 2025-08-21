

from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename
import os
import cv2
import sys
import json
import logging
logging.basicConfig(level=logging.DEBUG)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model import OCR_Model

api_bp = Blueprint('api', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../static/uploads/')
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), '../static/results/')




# Use EasyOCR for OCR recognition
@api_bp.route('/imageupload', methods=['POST'])
def image_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'no selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(img_path)
        try:
            annotated_image, text_output = OCR_Model.predict(img_path)
            # Save the annotated image
            annotated_image_filename = 'annotated_' + filename
            annotated_image_path = os.path.join(RESULTS_FOLDER, annotated_image_filename)
            cv2.imwrite(annotated_image_path, annotated_image)
            # Extract just the text from the OCR output
            extracted_text = [t[1] for t in text_output]
            # Save the extracted text to a results file
            result_txt_path = os.path.join(RESULTS_FOLDER, 'result.txt')
            with open(result_txt_path, 'w') as result_file:
                result_file.write("\n".join(extracted_text))
            return jsonify({
                'text': extracted_text,
                'annotated_image': annotated_image_filename
            })
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logging.error(f"Error processing image upload: {e}\n{tb}")
            return jsonify({'error': f'Processing failed: {str(e)}', 'traceback': tb}), 500
    return jsonify({'error': 'unknown error'}), 500

#         # Extract just the text from the OCR output
#         extracted_text = [t[1] for t in text_output]
        
#         # Save the extracted text to a results file
#         result_txt_path = os.path.join(RESULTS_FOLDER, 'result.txt')
#         with open(result_txt_path, 'w') as result_file:
#             result_file.write("\n".join(extracted_text))
        
#         return jsonify({
#             'text': extracted_text,
#             'annotated_image': annotated_image_filename
#         })

# @api_bp.route('/test', methods=['GET'])
# def test_route():
#     return "Test route is working!"

# def handle(path):
#     # Your API logic here
#     pass

from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import sys
import json
import logging

logging.basicConfig(level=logging.DEBUG)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model import OCR_Model

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

    # Extract just the text from the OCR output
    extracted_text = [t[1] for t in text_output]
    
    # Save the extracted text to a results file
    result_txt_path = os.path.join(RESULTS_FOLDER, 'result.txt')
    with open(result_txt_path, 'w') as result_file:
        result_file.write("\n".join(extracted_text))
    
    return jsonify({
        'text': extracted_text,
        'annotated_image': annotated_image_filename
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