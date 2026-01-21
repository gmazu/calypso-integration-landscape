import pandas as pd
import requests
import io

# Nueva URL proporcionada por el usuario
SHEET_ID = "1ePBXKfmFIZjNziSt23DDqF5qmAB8L0xX"
GID = "553561166"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

def exportar_gantt_bci_completo():
    print(f"📡 Conectando a la nueva URL: {SHEET_ID}...")
    try:
        # Descarga de datos
        response = requests.get(URL)
        response.raise_for_status()
        
        # Cargar CSV (usamos utf-8 para tildes y caracteres especiales)
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        # Función para definir Niveles (0-4)
        def determinar_nivel(id_val, nombre):
            nombre = str(nombre).strip()
            # Nivel 0: Raíz del proyecto
            if id_val == 1: return 0
            # Nivel 1: Grandes bloques de ambiente o hitos finales
            if any(x in nombre for x in ["Ambiente", "Paso a Producción", "Cluster ACM"]): return 1
            # Nivel 2: Fases principales (Habilitación, Plan, etc.)
            fases_principales = [3, 6, 17, 21, 29, 37, 45, 51, 59, 66, 81, 99, 135, 200, 224]
            if id_val in fases_principales: return 2
            # Nivel 3: Agrupadores específicos (Datacenters, Sub-fases)
            agrupadores = [82, 90, 104, 111, 217]
            if id_val in agrupadores: return 3
            # Nivel 4: Tareas y subtareas detalladas
            # Por defecto, si está en el bloque de producción detallado
            if id_val > 82 and id_val < 200: return 4
            return 3

        processed_rows = []
        # Iteramos sobre TODAS las filas del DataFrame sin filtros
        for index, row in df.iterrows():
            try:
                # Intentamos obtener el ID como número
                id_v = int(row.iloc[0])
                nombre_org = str(row.iloc[1])
                
                # Calculamos el nivel
                nivel = determinar_nivel(id_v, nombre_org)
                
                # Formateamos el nombre con 4 espacios por nivel
                nombre_identado = ("    " * nivel) + nombre_org
                
                # Estructura: [ID, Nivel, Nombre de Tarea, Estado, Asignado, Inicio, Fin, Avance, Duración, Predecesores]
                # row.iloc[2] en adelante corresponden a las columnas del sheet
                new_row = [
                    id_v, nivel, nombre_identado, 
                    row.iloc[2] if len(row) > 2 else "", # Estado
                    row.iloc[3] if len(row) > 3 else "", # Asignado
                    row.iloc[4] if len(row) > 4 else "", # Inicio
                    row.iloc[5] if len(row) > 5 else "", # Fin
                    row.iloc[6] if len(row) > 6 else "", # Avance
                    row.iloc[7] if len(row) > 7 else "", # Duración
                    row.iloc[8] if len(row) > 8 else ""  # Predecesores
                ]
                processed_rows.append(new_row)
            except (ValueError, TypeError):
                # Si la primera celda no es un número (cabeceras o filas vacías), la saltamos
                continue

        # Crear DataFrame final
        cols = ["ID", "Nivel", "Nombre de Tarea", "Estado", "Asignado", "Inicio", "Fin", "Avance", "Duración", "Predecesores"]
        df_final = pd.DataFrame(processed_rows, columns=cols)
        
        # Guardar archivo completo
        output_name = "Gantt_Completo_Identado_BCI.csv"
        df_final.to_csv(output_name, index=False, encoding='utf-8-sig')
        
        print(f"✅ ¡Éxito! Se procesaron {len(processed_rows)} filas.")
        print(f"📂 Archivo generado: {output_name}")

    except Exception as e:
        print(f"❌ Error al procesar: {e}")

if __name__ == "__main__":
    exportar_gantt_bci_completo()
