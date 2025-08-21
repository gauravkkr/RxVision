# RXvision

# Handwritten Digit Character Recognition and Note Conversion
<h3>A web application that allows users to recognize handwritten digits and convert handwritten notes into digital text. 
  This project uses React.js for the frontend, Flask for the backend, and machine learning for handwritten character recognition. Uses MNIST Dataset for training</h3>

## Table of Contents

## Features
  
## Technologies Used
   ### Project Structure
project-repo/
├── frontend/         # Contains React.js frontend code
│   ├── src/
│   └── public/
├── backend/          # Contains Flask backend API
│   ├── app/
│   └── tests/
├── data-science/     # Contains machine learning models and scripts
│   ├── models/
│   └── notebooks/
├── cloud/            # Deployment and infrastructure configurations
│   ├── aws/
│   └── ci-cd/
└── README.md         # Project documentation

## Setup and Installation

### Prerequisites

### Frontend Setup
   Clone the repository:
   git clone https://github.com/gauravkkr/RxVision
   cd OCR-project/frontend<br>
   See Frontend Readme for more details

 ###  Backend Setup
Navigate to the backend directory:
   cd ../backend
Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
Install backend dependencies:
   pip install -r requirements.txt
Start the Flask API:
   flask run

   ###  Machine Learning Model Setup:
   Navigate to the data-science directory:
      cd ../data-science
   Install required libraries:
      pip install -r requirements.txt
   Train the model 
   ### **Usage**
   - **Frontend:** Open [http://localhost:5173](http://localhost:5173) in your browser to access the React application.
   - **Backend:** The Flask API runs on [http://localhost:8080](http://localhost:8080). You can test it using tools like Postman.
   - **Machine Learning:** The pre-trained model is used to predict handwritten digits and convert notes.

## Team
  
   ### Acknowledgements
RXvision

A full-stack Handwriting Recognition and OCR web application.

---

## Tech Stack

- **Frontend:** React (Vite, Tailwind CSS)
- **Backend:** Python (Flask, EasyOCR, OpenCV)
- **Other:** PowerShell (for build automation), CORS, REST API

---

## Project Structure

```
RXvision/
│
├── backend/
│   ├── model/                # ML/AI model code
│   │   ├── __init__.py
│   │   └── model.py
│   ├── src/
│   │   ├── api.py            # Flask API endpoints
│   │   ├── app.py            # Flask app entrypoint
│   │   └── requirements.txt  # Python dependencies
│   └── static/
│       ├── results/          # OCR results (images/text)
│       └── uploads/          # Uploaded images
│
├── frontend/
│   ├── src/                  # React source code
│   ├── public/               # Static assets
│   ├── dist/                 # Production build output (after build)
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite config (with API proxy)
│
├── copy-frontend-build.ps1   # Script to copy frontend build to backend static
├── README.md                 # This file
└── ...
```

---

## Setup & Installation

### 1. Clone the repository
```
git clone <repo-url>
cd RXvision
```

### 2. Backend Setup (Python)
- Install Python 3.8+
- Install dependencies:
```
cd backend/src
pip install -r requirements.txt
```

### 3. Frontend Setup (React)
- Install Node.js (v16+ recommended)
- Install dependencies:
```
cd ../../frontend
npm install
```

---

## How to Run

### 1. Start the Backend (Flask)
```
cd backend/src
python app.py
```
- The backend will run at http://localhost:8080

### 2. Build and Deploy the Frontend
- Make your changes in `frontend/src`.
- Build the frontend:
```
cd ../../frontend
npm run build
```
- Copy the build to the backend static folder:
```
cd ..
powershell -ExecutionPolicy Bypass -File copy-frontend-build.ps1
```

### 3. Access the App
- Open http://localhost:8080 in your browser. The backend will serve the latest frontend build.

---

## Development Tips
- For live frontend development, use:
```
cd frontend
npm run dev
```
- API requests from the dev server are proxied to Flask (see `vite.config.js`).
- Always rebuild and copy the frontend build before deploying or testing with Flask.

---

## Troubleshooting
- If frontend changes do not appear, ensure you:
   1. Run `npm run build` in `frontend`
   2. Run the PowerShell script to copy the build
- If you get CORS errors, check the Flask CORS config and Vite proxy settings.

---

## Authors
- Team CapsLock

---

## License
[MIT] or your preferred license.
