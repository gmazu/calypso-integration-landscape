# Smartsheet to CSV Converter

Convierte archivos XML de MS Project a CSV con estructura Gantt, extrayendo los niveles de jerarquía reales.

## Uso Rápido

```bash
# Mostrar ayuda
python3 smartsheet2csv.py

# Procesar XML (genera smartsheet2csv.TIMESTAMP.csv en directorio actual)
python3 smartsheet2csv.py -xml "archivo.xml"

# Especificar directorio de salida (genera smartsheet2csv.TIMESTAMP.csv ahí)
python3 smartsheet2csv.py -xml "archivo.xml" -out /ruta/directorio/

# Especificar nombre de archivo de salida
python3 smartsheet2csv.py -xml "archivo.xml" -out "mi_gantt.csv"
```

## Opciones de Salida (-out)

| Uso | Resultado |
|-----|-----------|
| Sin `-out` | `./smartsheet2csv.YYYYMMDD_HHMMSS.csv` |
| `-out /tmp/` | `/tmp/smartsheet2csv.YYYYMMDD_HHMMSS.csv` |
| `-out /tmp/mi_archivo.csv` | `/tmp/mi_archivo.csv` |

## Formato de Salida

El CSV generado tiene las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| ID | Identificador de la tarea |
| Nivel | Nivel jerárquico (0=proyecto, 1=fase, 2=subfase, etc.) |
| Nombre de Tarea | Nombre de la tarea (sin indentación, el nivel indica jerarquía) |
| Estado | Completo / En progreso / No se ha iniciado |
| Asignado | Recursos asignados a la tarea |
| Inicio | Fecha de inicio (DD/MM/YY) |
| Fin | Fecha de fin (DD/MM/YY) |
| Avance | Porcentaje completado (ej: 50%) |
| Duración | Duración en días (ej: 5d, 1.5d) |
| Predecesores | IDs de tareas predecesoras |

## Mecánica XML vs XLS

### El Problema

Cuando exportas desde Smartsheet o Google Sheets a **XLS/CSV**, pierdes la información de **niveles de jerarquía** (el agrupador con +/-). Solo el **XML de MS Project** conserva esta información en el campo `<OutlineLevel>`.

### Flujo Recomendado

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLUJO DE TRABAJO                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. INICIAL (una vez o cuando cambie estructura)                │
│     ┌──────────┐         ┌──────────────────┐                  │
│     │   XML    │ ──────► │ smartsheet2csv   │ ──► CSV base     │
│     │ (tiene   │         │    -xml          │     (con niveles)│
│     │ niveles) │         └──────────────────┘                  │
│     └──────────┘                                                │
│                                                                 │
│  2. ACTUALIZACIONES (frecuente)                                 │
│     ┌──────────┐         ┌──────────────────┐                  │
│     │   XLS    │ ──────► │ smartsheet2csv   │ ──► CSV updated  │
│     │ (datos   │         │    -xls          │     (niveles del │
│     │ frescos) │         │                  │      CSV base)   │
│     └──────────┘         └──────────────────┘                  │
│                                                                 │
│  3. TAREAS NUEVAS DETECTADAS                                    │
│     ⚠️  Si el XLS tiene tareas que no están en el CSV base:     │
│     → Se muestra alerta                                         │
│     → Necesitas exportar nuevo XML para obtener niveles         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ID vs UID

MS Project asigna dos identificadores a cada tarea:

| Campo | Descripción | ¿Cambia? |
|-------|-------------|----------|
| `ID` | Número de fila (1, 2, 3...) | SÍ, si mueves/eliminas tareas |
| `UID` | Identificador único interno | NO, es estable |

**Recomendación:** Usar `UID` como identificador principal para hacer match entre XML y XLS, ya que no cambia aunque reorganices las tareas.

### Cómo Obtener el XML

1. **Desde Smartsheet:**
   - Archivo → Exportar → Microsoft Project (.xml)

2. **Desde MS Project:**
   - Archivo → Guardar como → XML

3. **Desde Google Sheets:**
   - No soporta exportación a XML de Project
   - Debes exportar primero a Excel y abrirlo en Project

### Estructura del XML de MS Project

```xml
<Project>
    <Tasks>
        <Task>
            <UID>1</UID>                    <!-- ID único estable -->
            <ID>1</ID>                      <!-- Número de fila -->
            <Name>Mi Tarea</Name>
            <OutlineLevel>2</OutlineLevel>  <!-- NIVEL DE JERARQUÍA -->
            <Start>2026-01-06T00:00:00</Start>
            <Finish>2026-01-10T00:00:00</Finish>
            <Duration>PT32H0M0S</Duration>  <!-- 4 días x 8 horas -->
            <PercentComplete>50</PercentComplete>
            <PredecessorLink>
                <PredecessorUID>5</PredecessorUID>
            </PredecessorLink>
        </Task>
    </Tasks>
    <Resources>
        <Resource>
            <UID>1</UID>
            <Name>Juan Pérez</Name>
        </Resource>
    </Resources>
    <Assignments>
        <Assignment>
            <TaskUID>1</TaskUID>
            <ResourceUID>1</ResourceUID>
        </Assignment>
    </Assignments>
</Project>
```

## Ejemplo de Salida

```csv
ID,Nivel,Nombre de Tarea,Estado,Asignado,Inicio,Fin,Avance,Duración,Predecesores
1,0,Proyecto Calypso BCI,En progreso,,06/01/26,29/04/26,8%,81.5d,
2,1,Ambiente Pre Productivo,En progreso,,06/01/26,29/04/26,8%,81.5d,
3,2,Kick off y requerimientos,Completo,,06/01/26,06/01/26,100%,1d,
4,3,Inicio formal del proyecto,Completo,,06/01/26,06/01/26,100%,1d,
```

## Requisitos

- Python 3.8+
- pandas (`pip install pandas`)
- openpyxl (`pip install openpyxl`) - solo para modo XLS (pendiente)

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `smartsheet2csv.py` | Script principal |
| `smartsheet2csv.TIMESTAMP.csv` | CSV generado (nombre por defecto) |
| `README.md` | Esta documentación |
