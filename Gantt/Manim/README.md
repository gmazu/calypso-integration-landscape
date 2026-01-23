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

## Pendientes
- [ ] Definir y documentar el criterio exacto de “contexto” al filtrar por ID.
- [x] Implementar filtros internos solo-XLSX con `--nivel` y `--id` (sin `--scope`).
- [x] Implementar salida de estadística previa para evitar escenas saturadas.
- [x] Crear `gantt_timeline_v2.py` (mantener `gantt_timeline.py` intacto).
- [ ] Implementar backup del XLSX junto al MP4 con timestamp y mismo nombre base.

## Hecho
- [x] Lectura de XLSX con indentación (alignment.indent) para niveles.
