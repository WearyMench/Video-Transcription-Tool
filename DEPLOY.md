# Despliegue en Render

## Configuración en Render Dashboard

1. **Crear nuevo Web Service**
   - Ve a tu dashboard de Render
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub

2. **Configuración del servicio:**
   - **Name**: `video-transcription-tool`
   - **Environment**: **Docker** ⚠️ (IMPORTANTE: Selecciona Docker, NO Python)
   - **Dockerfile Path**: `Dockerfile`
   - **Health Check Path**: `/health`

3. **Click en "Create Web Service"**

## Notas

- El Dockerfile usa Python 3.11 (compatible con Whisper)
- FFmpeg se instala automáticamente
- El modelo Whisper se descarga en el primer inicio (~150MB, puede tardar varios minutos)
- Render asigna el puerto automáticamente (la app lo lee de la variable `PORT`)

## Solución de Problemas

**Error: "KeyError: '__version__'"**
- Render está usando Python 3.13 en lugar de Docker
- **Solución**: Asegúrate de seleccionar "Docker" como Environment en Render

**Error: "FFmpeg not found"**
- El Dockerfile instala FFmpeg automáticamente
- Si ocurre, verifica que estés usando Docker y no Python nativo
