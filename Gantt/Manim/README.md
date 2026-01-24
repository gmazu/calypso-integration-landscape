# Gantt Manim

## Ejecución (flujo actual)
1) Generar `filter_gantt.tasks`:
```
python3 /home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/Gantt/Manim/gantt_timeline_v2.py -xlsx "/home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/GoogleDrive/Gantt BCI CALYPSO BANCO GLOBAL 2.0 (2).xlsx" --nivel 1
```
Para múltiples niveles: `--nivel 1 --nivel 2` o `--nivel 1,2`.
Los filtros `--nivel` y `--id` se aplican en el orden escrito (anidados).
También puedes usar separadores con `|` para indicar pasos; en shell usa `\|` o comillas para pasar el literal.
Usa `--expand` junto con `--id` para abrir solo el siguiente nivel del ID.

2) Renderizar con Manim (lee `filter_gantt.tasks`):
```
manim -pql gantt_timeline_v2.py GanttTimelineLevel2
```

## Ejecución (pipeline)
Genera `filter_gantt.tasks` y luego renderiza en un solo comando:
```
python3 /home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/Gantt/Manim/run_gantt_pipeline.py --xlsx "/home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/GoogleDrive/Gantt BCI CALYPSO BANCO GLOBAL 2.0 (2).xlsx" --nivel 1 --scene GanttTimelineLevel2 --quality pql --preview
```
Opcional: guardar el último render en otra ruta con timestamp:
```
python3 /home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/Gantt/Manim/run_gantt_pipeline.py --xlsx "/home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/GoogleDrive/Gantt BCI CALYPSO BANCO GLOBAL 2.0 (2).xlsx" --scene GanttTimelineLevel2 --quality pql --keep-scene /home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/GoogleDrive/Gantt/OUT
```

## Cambios recientes
- Línea de tiempo lee solo `filter_gantt.tasks`; XLSX se procesa aparte.
- Filtros en orden y soporte de `|` para encadenar pasos.
- `--expand` abre el siguiente nivel del ID desde el XLSX completo.
- Header toma título/subtítulo desde niveles 0/1 y la línea de tiempo usa niveles >= 2.
- Escala inferior tipo “mapa” con días y % promedio; fechas en el tick.
- Marcador “Hoy” con dial vintage (Real vs Plan) y tick sobre la línea principal.
- Barras de avance tipo ecualizador CRT con gradiente RGB y segmentos apagados visibles.
- Prueba de calidad: al final se llenan brevemente todos los ecualizadores.

## Pendientes
- [ ] Definir y documentar el criterio exacto de “contexto” al filtrar por ID.
- [x] Implementar filtros internos solo-XLSX con `--nivel` y `--id` (sin `--scope`).
- [x] Implementar salida de estadística previa para evitar escenas saturadas.
- [x] Crear `gantt_timeline_v2.py` (mantener `gantt_timeline.py` intacto).
- [ ] Implementar backup del XLSX junto al MP4 con timestamp y mismo nombre base.
- [ ] Agregar líneas de tiempo finales (inicio→fin) arriba en la línea superior.
- [ ] Poner nombre/etiqueta a las líneas de tiempo superior e inferior.
- [ ] Hacer pruebas (casos con filtros `--id/--nivel/--expand`).
- [ ] Agregar curva de rendimiento (cálculo de velocidad de avance) y pendiente para estimar fecha fin; la proyección debe ser ≤ fecha fin.
- [ ] Subir una copia del video a una cuenta privada de YouTube (pendiente de crearla).
- [ ] Ajustar ecualizador de % avance: 100% debe llegar al tope; sin bordes, barras horizontales estilo CRT, con gradiente cromático de rojo→verde y 0% en blanco (ref: `Images/940fafb26928fac30b9ce90e60eb67f7.jpg`).

## Contexto
- [ ] Esperar y pedir VB antes de hacer cambios.

## Calendario feriados 2026 (Chile)
Fuente:
```
https://www.gob.cl/noticias/feriados-2026-revisa-cuantos-habra-y-cuales-son-irrenunciables/
```
Lista de feriados 2026:
- 2026-01-01: Año Nuevo (irrenunciable)
- 2026-04-03: Viernes Santo
- 2026-04-04: Sábado Santo
- 2026-05-01: Día del Trabajo (irrenunciable)
- 2026-05-21: Día de las Glorias Navales
- 2026-06-21: Día Nacional de los Pueblos Indígenas
- 2026-06-29: San Pedro y San Pablo
- 2026-07-16: Día de la Virgen del Carmen
- 2026-08-15: Asunción de la Virgen
- 2026-09-18: Independencia Nacional (irrenunciable)
- 2026-09-19: Día de las Glorias del Ejército (irrenunciable)
- 2026-10-12: Encuentro de Dos Mundos
- 2026-10-31: Día Nacional de las Iglesias Evangélicas
- 2026-11-01: Día de Todos los Santos
- 2026-12-08: Inmaculada Concepción
- 2026-12-25: Navidad (irrenunciable)

## Hecho
- [x] Lectura de XLSX con indentación (alignment.indent) para niveles.

## Integracion con YouTube
Pasos (API oficial YouTube Data v3):
1) Crear proyecto en Google Cloud y habilitar YouTube Data API v3.
2) Configurar pantalla de consentimiento OAuth (agregar usuario de prueba si aplica).
3) Crear credenciales OAuth "Desktop App" y descargar `client_secret.json`.
4) Instalar dependencias:
```
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```
5) Usar el script oficial `upload_video.py` (ejemplo de Google) para subir videos.

Comando de ejemplo:
```
python upload_video.py \
  --file="/ruta/a/video.mp4" \
  --title="Mi Gantt" \
  --description="Render Manim" \
  --keywords="gantt,manim" \
  --category="22" \
  --privacyStatus="private"
```

Referencias oficiales:
```
https://developers.google.com/youtube/v3/guides/uploading_a_video
https://developers.google.com/youtube/v3/guides/auth/installed-apps
```
