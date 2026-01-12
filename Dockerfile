FROM python:3.11-slim

# Install FFmpeg and system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY index.html .

# Create necessary directories
RUN mkdir -p uploads outputs

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
