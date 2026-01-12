#!/usr/bin/env bash
set -e

# Install FFmpeg
echo "Installing FFmpeg..."
apt-get update
apt-get install -y ffmpeg

# Verify FFmpeg installation
ffmpeg -version

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
