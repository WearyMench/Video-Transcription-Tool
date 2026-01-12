# Deploy to Render

## Configuration in Render Dashboard

1. **Create new Web Service**

   - Go to your Render dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Service configuration:**

   - **Name**: `video-transcription-tool`
   - **Environment**: **Docker** ⚠️ (IMPORTANT: Select Docker, NOT Python)
   - **Dockerfile Path**: `Dockerfile`
   - **Health Check Path**: `/health`

3. **Click "Create Web Service"**

## Notes

- The Dockerfile uses Python 3.11 (compatible with Whisper)
- FFmpeg is installed automatically
- The Whisper model downloads on first startup (~150MB, may take several minutes)
- Render assigns the port automatically (the app reads it from the `PORT` environment variable)

## Troubleshooting

**Error: "KeyError: '**version**'"**

- Render is using Python 3.13 instead of Docker
- **Solution**: Make sure to select "Docker" as Environment in Render

**Error: "FFmpeg not found"**

- The Dockerfile installs FFmpeg automatically
- If this occurs, verify you're using Docker and not native Python
