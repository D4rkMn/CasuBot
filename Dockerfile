# Use the Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install FFmpeg and other required dependencies
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Run the application
CMD ["python", "main.py"]
