# YouTube Live (Gantt)

## Requisitos
- OBS instalado (para emitir) o ffmpeg.
- Credenciales OAuth de YouTube (`client_secret.json`).
- YouTube Data API v3 habilitada en Google Cloud.

## Archivos
- `youtube_live_setup.py`: crea un live broadcast + live stream y entrega la URL y stream key.
- `.secret` (ruta recomendada): archivo OAuth (`client_secret.json`).

## Crear live automáticamente
Ejemplo:
```
python3 youtube_live_setup.py \
  --client-secret /home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/Gantt/Manim/youtube/.secret \
  --title "Gantt Calypso BCI" \
  --description "Render Manim" \
  --privacy private \
  --latency normal
```
Esto genera `.live_stream.json` con:
- `ingest_address`
- `stream_name`
- `watch_url`

## Emitir el video (OBS)
1) Settings → Stream
   - Service: YouTube - RTMPS
   - Server: `ingest_address`
   - Stream Key: `stream_name`
2) Agrega Media Source con el MP4 y Start Streaming.

## Emitir por línea de comandos (ffmpeg)
```
ffmpeg -re -stream_loop -1 -i /ruta/al/video.mp4 \
  -c:v libx264 -preset veryfast -b:v 6000k -maxrate 6000k -bufsize 12000k \
  -c:a aac -b:a 128k -ar 44100 -f flv \
  "INGEST_ADDRESS/STREAM_NAME"
```

## Notas
- YouTube no permite reemplazar el archivo de un video existente manteniendo la misma URL.
- Para URL estable, usar Live o Playlist.
