from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from api import api_bp  # Import the API blueprint

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__),'..','..', 'frontend', 'dist'), static_url_path='/')

# #print("Static folder path:", os.path.join(os.path.dirname(__file__),'..', '..', 'frontend', 'dist'))
# # @app.route('/', defaults={'path': ''})
# # @app.route('/<path:path>')
# # @app.route('/static/<path:path>')
# # def serve_static(path):
# #     return send_from_directory(app.static_folder, path)


# Cleaned up Flask app for RXvision backend
from flask import Flask, send_from_directory, abort
import os
from flask_cors import CORS
from api import api_bp

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist'),
    static_url_path='/'
)

# Define the results folder path
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), '../static/results')

# Serve files from the results folder
@app.route('/results/<path:filename>')
def serve_result(filename):
    return send_from_directory(RESULTS_FOLDER, filename)

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Catch-all route to serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Let Flask handle API and static routes
    if path.startswith('api/') or path.startswith('static/') or path.startswith('results/'):
        return abort(404)
    # Serve static files if they exist
    full_path = os.path.join(app.static_folder, path)
    if path != '' and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve the React app's index.html
    return send_from_directory(app.static_folder, 'index.html')

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": "*"}, r"/results/*": {"origins": "*"}})

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)