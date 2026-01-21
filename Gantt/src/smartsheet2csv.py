import argparse
import io
import re
from urllib.parse import urlparse, parse_qs

import pandas as pd
import requests

def parse_gd_url(gd_url: str) -> tuple[str, str]:
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", gd_url)
    if not match:
        raise ValueError("No se pudo extraer el SHEET_ID de la URL.")
    sheet_id = match.group(1)

    parsed = urlparse(gd_url)
    qs = parse_qs(parsed.query)
    fragment_qs = parse_qs(parsed.fragment)
    gid = None
    if "gid" in qs and qs["gid"]:
        gid = qs["gid"][0]
    elif "gid" in fragment_qs and fragment_qs["gid"]:
        gid = fragment_qs["gid"][0]
    else:
        gid_match = re.search(r"gid=([0-9]+)", gd_url)
        if gid_match:
            gid = gid_match.group(1)

    if not gid:
        gid = "0"

    return sheet_id, gid

def generar_csv_local(gd_url: str):
    sheet_id, gid = parse_gd_url(gd_url)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    print("🚀 Conectando con Google Sheets...")
    try:
        # Descargar los datos
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        def find_col(patterns):
            for col in df.columns:
                col_lower = str(col).strip().lower()
                if any(p in col_lower for p in patterns):
                    return col
            return None

        col_id = find_col(["id"]) or df.columns[0]
        col_name = find_col(["nombre", "tarea", "task"]) or df.columns[1]
        col_estado = find_col(["estado"])
        col_asignado = find_col(["asignado"])
        col_inicio = find_col(["inicio"])
        col_fin = find_col(["final", "fin"])
        col_avance = find_col(["avance", "porcentaje"])
        col_duracion = find_col(["duracion"])
        col_predecesores = find_col(["predecesor"])

        # Función para definir el nivel (0-4)
        def definir_nivel(row):
            id_val = pd.to_numeric(row[col_id], errors="coerce")
            nombre = str(row[col_name]).strip()
            if id_val == 1:
                return 0
            if "Ambiente" in nombre:
                return 1
            if id_val in [3, 6, 17, 21, 29, 37, 45, 51, 59, 66, 81, 99, 135, 200]:
                return 2
            if id_val in [82, 90, 217]:
                return 3
            if pd.isna(id_val):
                return 4
            return 3 if id_val < 200 else 4

        processed_data = []
        for _, row in df.iterrows():
            id_val = row[col_id]
            nivel = definir_nivel(row)
            nombre_original = str(row[col_name])
            # Identación con 4 espacios
            nombre_identado = ("    " * nivel) + nombre_original

            estado = row[col_estado] if col_estado else row.iloc[2] if len(row) > 2 else ""
            asignado = row[col_asignado] if col_asignado else row.iloc[3] if len(row) > 3 else ""
            inicio = row[col_inicio] if col_inicio else row.iloc[4] if len(row) > 4 else ""
            fin = row[col_fin] if col_fin else row.iloc[5] if len(row) > 5 else ""
            avance = row[col_avance] if col_avance else row.iloc[6] if len(row) > 6 else ""
            duracion = row[col_duracion] if col_duracion else row.iloc[7] if len(row) > 7 else ""
            predecesores = row[col_predecesores] if col_predecesores else row.iloc[8] if len(row) > 8 else ""
            
            # Estructura: [ID, Nivel, Nombre, Estado, Asignado, Inicio, Fin, Avance, Duración, Predecesores]
            processed_data.append([
                id_val, nivel, nombre_identado, 
                estado, asignado, inicio,
                fin, avance, duracion, predecesores
            ])

        # Crear DataFrame final y exportar a CSV
        columnas = ["ID", "Nivel", "Nombre de Tarea", "Estado", "Asignado", "Inicio", "Fin", "Avance", "Duración", "Predecesores"]
        df_final = pd.DataFrame(processed_data, columns=columnas)
        df_final.to_csv("Gantt_Calypso_Local.csv", index=False, encoding='utf-8-sig')
        
        print("✅ Archivo 'Gantt_Calypso_Local.csv' generado con éxito.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporta un Google Sheet a CSV.")
    parser.add_argument(
        "-gdurl",
        required=True,
        help="URL de Google Sheets que contiene el sheetId y gid.",
    )
    args = parser.parse_args()
    generar_csv_local(args.gdurl)
