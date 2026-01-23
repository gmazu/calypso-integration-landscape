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
- [ ] Esperar VB antes de hacer cambios; agregar esto en la sección de contexto.
- [x] Implementar filtros internos solo-XLSX con `--nivel` y `--id` (sin `--scope`).
- [x] Implementar salida de estadística previa para evitar escenas saturadas.
- [x] Crear `gantt_timeline_v2.py` (mantener `gantt_timeline.py` intacto).
- [ ] Implementar backup del XLSX junto al MP4 con timestamp y mismo nombre base.
- [ ] Ajustar ecualizador de % avance: 100% debe llegar al tope; sin bordes, barras horizontales estilo CRT, con gradiente cromático de rojo→verde y 0% en blanco (ref: `Images/940fafb26928fac30b9ce90e60eb67f7.jpg`).

## Hecho
- [x] Lectura de XLSX con indentación (alignment.indent) para niveles.
