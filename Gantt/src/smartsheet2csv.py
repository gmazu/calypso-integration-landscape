#!/usr/bin/env python3
"""
Convierte un archivo XML de MS Project a CSV con estructura Gantt.
Extrae el OutlineLevel real del XML para mantener la jerarquía correcta.
"""
import argparse
import sys
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path

# Namespace de MS Project
NS = {'ms': 'http://schemas.microsoft.com/project'}

def parse_duration(duration_str: str) -> str:
    """Convierte duración ISO 8601 (PT8H0M0S) a formato legible (1d)."""
    if not duration_str or duration_str == 'PT0H0M0S':
        return '0'

    hours = 0
    if 'H' in duration_str:
        h_part = duration_str.split('H')[0].replace('PT', '')
        try:
            hours = int(h_part)
        except ValueError:
            return duration_str

    days = hours / 8  # 8 horas = 1 día laboral
    if days == int(days):
        return f"{int(days)}d"
    return f"{days:.1f}d"

def parse_date(date_str: str) -> str:
    """Convierte fecha ISO (2026-01-06T00:00:00) a formato DD/MM/YY."""
    if not date_str:
        return ''
    try:
        date_part = date_str.split('T')[0]
        year, month, day = date_part.split('-')
        return f"{day}/{month}/{year[2:]}"
    except (ValueError, IndexError):
        return date_str

def get_element_text(task, tag: str) -> str:
    """Obtiene el texto de un elemento XML o retorna cadena vacía."""
    elem = task.find(f'ms:{tag}', NS)
    return elem.text if elem is not None and elem.text else ''

def extract_tasks_from_xml(xml_path: str) -> list[dict]:
    """Extrae todas las tareas del XML de MS Project."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    tasks = []
    for task in root.findall('.//ms:Task', NS):
        uid = get_element_text(task, 'UID')
        task_id = get_element_text(task, 'ID')

        # Saltar tarea 0 (es el proyecto raíz en MS Project)
        if task_id == '0':
            continue

        name = get_element_text(task, 'Name')
        outline_level = get_element_text(task, 'OutlineLevel')
        start = parse_date(get_element_text(task, 'Start'))
        finish = parse_date(get_element_text(task, 'Finish'))
        duration = parse_duration(get_element_text(task, 'Duration'))
        percent_complete = get_element_text(task, 'PercentComplete')

        # Obtener predecesores
        predecessors = []
        for pred in task.findall('ms:PredecessorLink', NS):
            pred_uid = get_element_text(pred, 'PredecessorUID')
            if pred_uid:
                predecessors.append(pred_uid)

        # Estado basado en porcentaje
        pct = int(percent_complete) if percent_complete.isdigit() else 0
        if pct == 100:
            estado = 'Completo'
        elif pct > 0:
            estado = 'En progreso'
        else:
            estado = 'No se ha iniciado'

        # Formato de avance
        avance = f"{pct}%" if percent_complete else '0%'

        # Nivel (ajustamos -1 porque MS Project empieza en 1)
        nivel = int(outline_level) - 1 if outline_level.isdigit() else 0

        tasks.append({
            'ID': task_id,
            'Nivel': nivel,
            'Nombre de Tarea': name,
            'Estado': estado,
            'Asignado': '',  # El XML no tiene asignaciones en Tasks, están en Assignments
            'Inicio': start,
            'Fin': finish,
            'Avance': avance,
            'Duración': duration,
            'Predecesores': ','.join(predecessors) if predecessors else ''
        })

    return tasks

def extract_assignments(xml_path: str) -> dict[str, list[str]]:
    """Extrae las asignaciones de recursos por tarea."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Primero construir mapa de ResourceUID -> ResourceName
    resources = {}
    for res in root.findall('.//ms:Resource', NS):
        uid = get_element_text(res, 'UID')
        name = get_element_text(res, 'Name')
        if uid and name:
            resources[uid] = name

    # Luego mapear TaskUID -> lista de recursos asignados
    assignments = {}
    for assign in root.findall('.//ms:Assignment', NS):
        task_uid = get_element_text(assign, 'TaskUID')
        res_uid = get_element_text(assign, 'ResourceUID')

        if task_uid and res_uid and res_uid in resources:
            if task_uid not in assignments:
                assignments[task_uid] = []
            assignments[task_uid].append(resources[res_uid])

    return assignments

def xml_to_csv(xml_path: str, output_path: str) -> None:
    """Convierte XML de MS Project a CSV."""
    print(f"Leyendo XML: {xml_path}")

    tasks = extract_tasks_from_xml(xml_path)
    assignments = extract_assignments(xml_path)

    # Agregar asignaciones a las tareas
    for task in tasks:
        task_id = task['ID']
        if task_id in assignments:
            task['Asignado'] = ', '.join(assignments[task_id])

    # Crear DataFrame y exportar
    df = pd.DataFrame(tasks)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"CSV generado: {output_path} ({len(tasks)} tareas)")

def show_help():
    """Muestra ayuda detallada del script."""
    help_text = """
================================================================================
                        SMARTSHEET TO CSV CONVERTER
================================================================================

DESCRIPCION:
    Convierte archivos XML de MS Project a CSV con estructura Gantt.
    Extrae el OutlineLevel real del XML para mantener la jerarquia correcta.

USO:
    python3 smartsheet2csv.py -xml <archivo.xml> [-out <salida.csv>]

ARGUMENTOS:
    -xml, --xml-path    Ruta al archivo XML de MS Project (requerido)
    -out, --output      Nombre del CSV de salida (default: smartsheet2csv.TIMESTAMP.csv)

EJEMPLOS:
    # Procesar XML y generar CSV
    python3 smartsheet2csv.py -xml "Gantt BCI.xml"

    # Especificar nombre de salida
    python3 smartsheet2csv.py -xml "Gantt BCI.xml" -out "MiGantt.csv"

FORMATO DE SALIDA (CSV):
    ID, Nivel, Nombre de Tarea, Estado, Asignado, Inicio, Fin, Avance,
    Duracion, Predecesores

NOTAS:
    - El XML debe ser exportado desde MS Project o Smartsheet
    - Los niveles se extraen del campo <OutlineLevel> del XML
    - Las fechas se convierten a formato DD/MM/YY
    - La duracion se convierte a dias (ej: 5d, 1.5d)

Ver README.md para mas detalles sobre el flujo XML/XLS.
================================================================================
"""
    print(help_text)

def main():
    # Si no hay argumentos, mostrar ayuda
    if len(sys.argv) == 1:
        show_help()
        return 0

    parser = argparse.ArgumentParser(
        description='Convierte XML de MS Project a CSV con estructura Gantt.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejecuta sin argumentos para ver ayuda detallada.'
    )
    parser.add_argument(
        '-xml', '--xml-path',
        required=True,
        help='Ruta al archivo XML de MS Project'
    )
    parser.add_argument(
        '-out', '--output',
        default=None,
        help='Nombre del archivo CSV de salida (default: smartsheet2csv.TIMESTAMP.csv)'
    )

    args = parser.parse_args()

    if not Path(args.xml_path).exists():
        print(f"Error: No se encontro el archivo {args.xml_path}")
        return 1

    # Generar nombre con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"smartsheet2csv.{timestamp}.csv"

    if args.output is None:
        # Sin -out: crear en directorio actual
        output_path = default_filename
    elif Path(args.output).is_dir():
        # -out es directorio: crear archivo con nombre por defecto ahí
        output_path = str(Path(args.output) / default_filename)
    else:
        # -out es archivo: usar tal cual
        output_path = args.output

    xml_to_csv(args.xml_path, output_path)
    return 0

if __name__ == "__main__":
    exit(main())
