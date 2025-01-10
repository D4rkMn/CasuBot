# Use the Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install system dependencies for psycopg2, FFmpeg, and development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "main.py"]
