# Gantt Manim

## Ejecución (flujo actual)
1) Preprocesar desde XLSX (imprime `tasks = [...]`):
```
python3 /home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/Gantt/src/preprocess_gantt.py -xlsx "/home/gmazuel/eVΛ/BCI/Calypso/CalypsoBCI/GoogleDrive/Gantt BCI CALYPSO BANCO GLOBAL 2.0 (2).xlsx"
```

2) Renderizar con Manim:
```
manim -pql gantt_timeline.py GanttTimelineLevel2
```

## Pendientes
- [ ] Definir y documentar el criterio exacto de “contexto” al filtrar por ID.
- [ ] Implementar preprocesador solo-XLSX con `--nivel` y `--id` (sin `--scope`).
- [ ] Implementar salida de estadística previa para evitar escenas saturadas.
- [ ] Crear `gantt_timeline_v2.py` (mantener `gantt_timeline.py` intacto).
- [ ] Implementar backup del XLSX junto al MP4 con timestamp y mismo nombre base.

## Hecho
- [x] Lectura de XLSX con indentación (alignment.indent) para niveles.
