import os
import asyncio
import warnings
from pathlib import Path
from typing import Optional
import tempfile
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import whisper
import ffmpeg
import pandas as pd
from datetime import timedelta

# Suppress Whisper FP16 warning on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

app = FastAPI(title="Video Transcription Tool")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Load Whisper model (load once at startup)
MODEL_NAME = "base"  # Can be: tiny, base, small, medium, large
whisper_model = None

@app.on_event("startup")
async def load_model():
    global whisper_model
    print("Loading Whisper model...")
    whisper_model = whisper.load_model(MODEL_NAME)
    print("Model loaded successfully!")

def extract_audio_from_video(video_path: str, audio_path: str) -> None:
    """Extract audio from video file using ffmpeg."""
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")

def format_time(seconds: float) -> str:
    """Format seconds to HH:MM:SS format."""
    td = timedelta(seconds=int(seconds))
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def transcribe_audio_segments(audio_path: str, interval_seconds: int = 5) -> list:
    """Transcribe audio in specified interval segments."""
    print(f"Transcribing audio: {audio_path}")
    
    # Transcribe the entire audio
    result = whisper_model.transcribe(audio_path, word_timestamps=True)
    
    # Get audio duration
    probe = ffmpeg.probe(audio_path)
    duration = float(probe['streams'][0]['duration'])
    
    segments = []
    current_time = 0.0
    
    while current_time < duration:
        start_time = current_time
        end_time = min(current_time + interval_seconds, duration)
        
        # Find transcription text for this time segment
        segment_text = ""
        words_in_segment = []
        
        if 'segments' in result:
            for segment in result['segments']:
                seg_start = segment['start']
                seg_end = segment['end']
                
                # Check if segment overlaps with our time window
                if seg_start < end_time and seg_end > start_time:
                    # Get words in this segment that fall within our window
                    if 'words' in segment:
                        for word_info in segment['words']:
                            word_start = word_info['start']
                            word_end = word_info['end']
                            
                            # Include words that overlap with our interval
                            if word_start < end_time and word_end > start_time:
                                words_in_segment.append(word_info['word'].strip())
                    
                    # If no words found, use segment text
                    if not words_in_segment and 'text' in segment:
                        words_in_segment.append(segment['text'].strip())
        
        segment_text = " ".join(words_in_segment).strip()
        
        segments.append({
            'start_time': start_time,
            'end_time': end_time,
            'text': segment_text
        })
        
        current_time += interval_seconds
    
    return segments

def create_excel_output(video_name: str, segments: list, output_path: str) -> None:
    """Create Excel file with transcription data."""
    data = {
        'Video Name': [],
        'Start Time (hh:mm:ss)': [],
        'End Time (hh:mm:ss)': [],
        'Transcription': []
    }
    
    for segment in segments:
        data['Video Name'].append(video_name)
        data['Start Time (hh:mm:ss)'].append(format_time(segment['start_time']))
        data['End Time (hh:mm:ss)'].append(format_time(segment['end_time']))
        data['Transcription'].append(segment['text'])
    
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Excel file created: {output_path}")

@app.get("/")
async def root():
    """Serve the frontend."""
    return FileResponse("index.html")

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """Handle video upload and transcription."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file size (5GB = 5 * 1024 * 1024 * 1024 bytes)
    MAX_SIZE = 5 * 1024 * 1024 * 1024  # 5GB
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        video_path = temp_path / file.filename
        audio_path = temp_path / "audio.wav"
        
        # Save uploaded video
        file_size = 0
        with open(video_path, "wb") as buffer:
            while True:
                chunk = await file.read(8192)  # Read in chunks
                if not chunk:
                    break
                file_size += len(chunk)
                if file_size > MAX_SIZE:
                    raise HTTPException(status_code=400, detail="File size exceeds 5GB limit")
                buffer.write(chunk)
        
        print(f"Video uploaded: {file.filename} ({file_size / (1024*1024):.2f} MB)")
        
        try:
            # Extract audio
            print("Extracting audio...")
            extract_audio_from_video(str(video_path), str(audio_path))
            
            # Transcribe audio in 5-second intervals
            print("Transcribing audio...")
            segments = transcribe_audio_segments(str(audio_path), interval_seconds=5)
            
            # Create Excel file
            video_name = Path(file.filename).stem  # Filename without extension
            output_filename = f"{video_name}_transcription.xlsx"
            output_path = OUTPUT_DIR / output_filename
            
            print("Creating Excel file...")
            create_excel_output(video_name, segments, str(output_path))
            
            return JSONResponse({
                "message": "Transcription completed successfully",
                "filename": output_filename,
                "segments_count": len(segments)
            })
            
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download the generated Excel file."""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": whisper_model is not None}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
