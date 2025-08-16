# RXvision

# Handwritten Digit Character Recognition and Note Conversion
<h3>A web application that allows users to recognize handwritten digits and convert handwritten notes into digital text. 
  This project uses React.js for the frontend, Flask for the backend, and machine learning for handwritten character recognition. Uses MNIST Dataset for training</h3>

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contribution Guidelines](#contribution-guidelines)
- [Team](#team)

## Features
- Recognizes handwritten digits using a trained machine learning model.
- Converts handwritten notes into digital text.
- User-friendly web interface for uploading and viewing notes.
- RESTful API for backend communication.
- Cloud deployment using AWS.
  
## Technologies Used
- **Frontend:** React.js
- **Backend:** Flask (Python)
- **Machine Learning:** TensorFlow, Keras
- **Cloud:** AWS S3, AWS EC2, AWS Lambda
- **Version Control:** Git, GitHub
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
- [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/)
- [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)

### Frontend Setup
   Clone the repository:
   git clone https://github.com/your-repo/OCR-project.git<br>
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
- **Frontend Developer:** 
- **Backend Developer:** 
- **Data Scientist:** 
- **Cloud/Git Developer:** 
  
   ### Acknowledgements
- [React](https://reactjs.org/) - Frontend framework
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [TensorFlow](https://www.tensorflow.org/) - Machine learning library
- Special thanks to our mentors and collaborators.
