# Guía de Despliegue en Render

## Configuración en Render

### Opción 1: Usando Docker (Recomendado)

1. En el dashboard de Render, crea un nuevo **Web Service**
2. Conecta tu repositorio de GitHub
3. Configuración:
   - **Name**: video-transcription-tool
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.`
   - **Health Check Path**: `/health`

4. Variables de entorno (opcional):
   - `PORT`: 8000 (Render lo asigna automáticamente)

### Opción 2: Usando Python nativo

Si prefieres no usar Docker:

1. En el dashboard de Render, crea un nuevo **Web Service**
2. Conecta tu repositorio de GitHub
3. Configuración:
   - **Name**: video-transcription-tool
   - **Environment**: Python 3
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `python main.py`

4. Variables de entorno:
   - `PORT`: 8000 (Render lo asigna automáticamente)
   - `PYTHON_VERSION`: 3.11.9

## Notas Importantes

- **FFmpeg**: Se instala automáticamente en el Dockerfile o mediante build.sh
- **Python Version**: Usa Python 3.11 (no 3.13) para compatibilidad con Whisper
- **Modelo Whisper**: Se descarga automáticamente en el primer inicio (~150MB para el modelo base)
- **Tiempo de inicio**: El primer deploy puede tardar varios minutos debido a la descarga del modelo

## Solución de Problemas

### Error: "KeyError: '__version__'"
- **Causa**: Incompatibilidad con Python 3.13
- **Solución**: Usa Python 3.11 (ya configurado en runtime.txt y Dockerfile)

### Error: "FFmpeg not found"
- **Causa**: FFmpeg no está instalado
- **Solución**: Asegúrate de usar el Dockerfile o el build.sh que instala FFmpeg

### Error: "Model loading timeout"
- **Causa**: El modelo Whisper tarda en descargarse
- **Solución**: Espera unos minutos en el primer deploy. El modelo se cachea después.

## Recursos

- Render Docs: https://render.com/docs
- Docker en Render: https://render.com/docs/docker
