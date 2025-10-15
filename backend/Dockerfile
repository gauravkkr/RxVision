FROM python:3.11-slim

WORKDIR /app

# system deps for opencv and easyocr
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend source
COPY ./src /app
COPY ./model /app/model
COPY ./static /app/static

# Install Python deps
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# expose port
EXPOSE 8080

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "-w", "1"]
