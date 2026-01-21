import pandas as pd
import requests
import io

# Fuente de datos: Google Spreadsheet BCI/Global
SHEET_ID = "1ePBXKfmFIZjNziSt23DDqF5qmAB8L0xX"
GID = "553561166"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

def exportar_todo():
    print("📡 Descargando datos completos desde Google Sheets...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        # Leemos el CSV original
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        
        # Lógica de asignación de Niveles (0-4)
        def calcular_nivel(row):
            id_val = row.iloc[0]
            nombre = str(row.iloc[1]).strip()
            if id_val == 1: return 0
            if "Ambiente" in nombre: return 1
            # IDs de fases principales (Nivel 2)
            fases_ids = [3, 6, 17, 21, 29, 37, 45, 51, 59, 66, 81, 99, 135, 143, 153, 161, 174, 183, 200]
            if id_val in fases_ids: return 2
            # Agrupadores intermedios (Nivel 3)
            if id_val in [82, 90, 104, 111, 201, 208, 217]: return 3
            # Tareas detalladas (Nivel 4)
            return 4 if id_val > 82 else 3

        output = []
        for _, row in df.iterrows():
            try:
                id_v = int(row.iloc[0])
                nivel = calcular_nivel(row)
                nombre_org = str(row.iloc[1])
                # Aplicamos 4 espacios por cada nivel
                nombre_new = ("    " * nivel) + nombre_org
                
                # Estructura: [ID, Nivel, Nombre de Tarea, Estado, Asignado, Inicio, Fin, Avance, Duración, Predecesores]
                linea = [
                    id_v, nivel, nombre_new, 
                    row.iloc[2], row.iloc[3], row.iloc[4], 
                    row.iloc[5], row.iloc[6], row.iloc[7], row.iloc[8]
                ]
                output.append(linea)
            except: continue

        df_final = pd.DataFrame(output, columns=["ID", "Nivel", "Nombre de Tarea", "Estado", "Asignado", "Inicio", "Fin", "Avance", "Duración", "Predecesores"])
        
        # Exportación a CSV completo
        df_final.to_csv("Gantt_Completo_Identado.csv", index=False, encoding='utf-8-sig')
        print(f"✅ Se han procesado {len(output)} filas. Archivo guardado: Gantt_Completo_Identado.csv")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    exportar_todo()
