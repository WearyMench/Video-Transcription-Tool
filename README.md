# Video Transcription Tool

A web application that transcribes video files and exports the transcription to an Excel file with time-stamped segments.

## Features

- Upload video files up to 5GB
- Automatic audio extraction from video
- Transcription in 5-second intervals
- Excel export with columns:
  - Video Name
  - Start Time (hh:mm:ss)
  - End Time (hh:mm:ss)
  - Transcription

## Requirements

- Python 3.8+
- FFmpeg (must be installed on your system)

### Installing FFmpeg

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to PATH, or install via chocolatey: `choco install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## Installation

### Option 1: Using Virtual Environment (Recommended)

**Windows:**
1. Run setup script:
```bash
setup.bat
```

This will create the virtual environment and install all dependencies.

Or manually:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Global Installation (Not Recommended)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Note:** The Whisper model will be downloaded automatically on first run (base model ~150MB).

## Usage

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
1. Activate virtual environment:
```bash
source venv/bin/activate
```

2. Start the server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Upload a video file and wait for transcription to complete.

4. Download the generated Excel file.

## Configuration

You can change the Whisper model in `main.py`:
- `tiny` - Fastest, least accurate (~39MB)
- `base` - Balanced (default, ~150MB)
- `small` - Better accuracy (~500MB)
- `medium` - High accuracy (~1.5GB)
- `large` - Best accuracy (~3GB)

## Project Structure

```
.
├── main.py              # FastAPI backend
├── index.html           # Frontend UI
├── requirements.txt     # Python dependencies
├── setup.bat            # Setup script - creates venv and installs dependencies (Windows)
├── start.bat            # Start script - runs the application (Windows)
├── venv/                # Virtual environment directory (created by setup)
├── uploads/             # Temporary upload storage (auto-created)
└── outputs/             # Generated Excel files (auto-created)
```

## Notes

- Large video files may take significant time to process
- The transcription quality depends on audio clarity
- Processing happens server-side, so keep the browser tab open
