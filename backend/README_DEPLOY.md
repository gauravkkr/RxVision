# Deploying RXvision backend with Docker

Steps to build and run the backend container locally:

1. Build the image from `backend/`:

```powershell
cd backend
docker compose build
```

2. Run the service:

```powershell
docker compose up -d
```

3. The backend will be available at http://localhost:8080

Notes:
- The container uses `gunicorn` to serve the Flask app. It binds to port 8080.
- The image installs packages from `src/requirements.txt`. If you update dependencies, rebuild the image.
- For better OCR performance, add a GPU-enabled base image and set `easyocr` to use GPU.
