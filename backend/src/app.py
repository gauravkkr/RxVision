# from flask import Flask, send_from_directory
# import os
# from flask_cors import CORS
# from api import api_bp  # Import the API blueprint


# app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__),'..','..', 'frontend', 'dist'), static_url_path='/')

# #print("Static folder path:", os.path.join(os.path.dirname(__file__),'..', '..', 'frontend', 'dist'))
# # @app.route('/', defaults={'path': ''})
# # @app.route('/<path:path>')
# # @app.route('/static/<path:path>')
# # def serve_static(path):
# #     return send_from_directory(app.static_folder, path)

# RESULTS_FOLDER = '../static/results'

# @app.route('/results/<path:path>')
# def serve_results(path):
#     return send_from_directory(RESULTS_FOLDER, path)

# # @app.route('/static/results/<path:filename>')
# # def serve_results_file(filename):
# #     return send_from_directory(os.path.join(app.static_folder, 'results'), filename)
# # @app.route('/static/results/<path:filename>')
# # def serve_static_results(filename):
# #     return send_from_directory(os.path.join(app.static_folder, 'results'), filename)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     print(f"Requested path: {path}")
#     if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
#         return send_from_directory(app.static_folder, path)
#     return send_from_directory(app.static_folder, "index.html")

# # def catch_all(path):
# #     if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
# #         return send_from_directory(app.static_folder, path)
# #     return send_from_directory(app.static_folder,"index.html")
#         #return app.send_static_file(path)
#     #return app.send_static_file('index.html')


# # Enable CORS for API requests
# CORS(app, resources={r"/api/": {"origins": ["http://localhost:5173"]}})
# CORS(app, resources={r"/static/*": {"origins": "http://127.0.0.1:8080"}})
# CORS(app, resources={r"/results/*": {"origins": "*"}})

# # Register the API blueprint
# app.register_blueprint(api_bp, url_prefix='/api')

# # Serve the frontend React build for any non-API routes
# # @app.route('/')
# # @app.route('/<path:path>')
# # def serve_react_app(path=''):
# #     # Serve index.html for all routes except /api routes
# #     return send_from_directory(os.path.join(os.pardir, 'frontend', 'dist'), 'index.html')

# # CORS after request handler (in case it's needed)
# @app.after_request
# def after_request(response):
#     #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
#     return response

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=8080)

# @app.route('/test_static')
# def test_static():
#     return send_from_directory(os.path.join(os.pardir, os.pardir, 'frontend', 'dist'), 'index.html')



# from flask import Flask, send_from_directory
# import os
# from flask_cors import CORS
# from api import api_bp

# app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist'), static_url_path='/')

# # Define the results folder path
# RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), '../static/results')

# # Serve files from the results folder
# @app.route('/results/<path:filename>')
# def serve_result(filename):
#     return send_from_directory(RESULTS_FOLDER, filename)

# # Catch-all route to serve the React app
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
#         return send_from_directory(app.static_folder, path)
#     return send_from_directory(app.static_folder, 'index.html')

# # Configure CORS
# CORS(app, resources={r"/api/*": {"origins": "*"}, r"/results/*": {"origins": "*"}})

# # Register the API blueprint
# app.register_blueprint(api_bp, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=8080)

from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from api import api_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist'), static_url_path='/')

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
    if path.startswith('api/'):
        # Let the API blueprint handle API routes
        return api_bp.handle(path[4:])
    # For all other routes, serve the index.html file
    return send_from_directory(app.static_folder, 'index.html')

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": "*"}, r"/results/*": {"origins": "*"}})

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)