import pandas as pd
import requests
import io
import sys

# URL de exportación del nuevo Google Sheet
SHEET_ID = "1ePBXKfmFIZjNziSt23DDqF5qmAB8L0xX"
GID = "553561166"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

def procesar_gantt_v4():
    print(f"📡 Conectando a Google Sheets...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        # Leemos los datos sin asumir nombres de columnas fijos
        raw_data = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        
        if raw_data.empty:
            print("❌ El archivo descargado está vacío. Revisa los permisos del Google Sheet.")
            return

        print(f"✅ Datos recibidos: {len(raw_data)} filas detectadas.")
        print(f"DEBUG: Columnas encontradas: {list(raw_data.columns)}")

        processed_rows = []

        for index, row in raw_data.iterrows():
            # Extraemos el ID y el Nombre (asumimos que son las dos primeras columnas)
            raw_id = str(row.iloc[0]).strip()
            nombre_tarea = str(row.iloc[1]).strip()

            # Saltamos filas de cabecera que Google a veces repite o filas vacías
            if raw_id.lower() in ['id', 'nan', '']:
                continue

            # Determinación de Nivel (0-4)
            # Intentamos convertir ID a entero para la lógica, si no, nivel 3 por defecto
            try:
                id_int = int(float(raw_id))
            except:
                id_int = 999 

            # Lógica de Niveles optimizada
            nivel = 3
            if id_int == 1: nivel = 0
            elif "Ambiente" in nombre_tarea or "Paso a Producción" in nombre_tarea: nivel = 1
            elif id_int in [3, 6, 17, 21, 29, 37, 45, 51, 59, 66, 81, 99, 135, 200]: nivel = 2
            elif id_int in [82, 90, 217]: nivel = 3
            elif id_int > 82 and id_int < 200: nivel = 4

            # Formatear nombre con identación
            nombre_identado = ("    " * nivel) + nombre_tarea
            
            # Construir la fila final con todas las columnas disponibles
            # Estructura: [ID, Nivel, Nombre, Estado, Asignado, Inicio, Fin, Avance, Duración, Predecesores]
            new_row = [
                raw_id,
                nivel,
                nombre_identado,
                row.iloc[2] if len(row) > 2 else "",
                row.iloc[3] if len(row) > 3 else "",
                row.iloc[4] if len(row) > 4 else "",
                row.iloc[5] if len(row) > 5 else "",
                row.iloc[6] if len(row) > 6 else "",
                row.iloc[7] if len(row) > 7 else "",
                row.iloc[8] if len(row) > 8 else ""
            ]
            processed_rows.append(new_row)

        # Crear y guardar el CSV
        columnas = ["ID", "Nivel", "Nombre de Tarea", "Estado", "Asignado", "Inicio", "Fin", "Avance", "Duración", "Predecesores"]
        df_final = pd.DataFrame(processed_rows, columns=columnas)
        
        output_name = "Gantt_Calypso_Completo_v4.csv"
        df_final.to_csv(output_name, index=False, encoding='utf-8-sig')
        
        print(f"🚀 ¡Éxito! Se procesaron {len(processed_rows)} filas.")
        print(f"📂 Archivo generado: {output_name}")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    procesar_gantt_v4()
