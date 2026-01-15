# Guía para la Nomenclatura de Servidores

Este documento establece la convención estándar para nombrar los servidores dentro del proyecto, asegurando que los nombres sean consistentes, informativos y fáciles de entender.

## Estructura del Nombre

El nombre de cada servidor se compone de seis partes separadas por guiones, siguiendo la estructura:

`[OS]-[ENTORNO]-[APLICACION]-[ROL]-[UBICACION]-[SECUENCIA]`

---

### 1. Sistema Operativo (OS)

Indica el sistema operativo principal del servidor.

| Código | Descripción |
| :--- | :--- |
| `lnx` | Linux |
| `win` | Windows |

---

### 2. Entorno (ENTORNO)

Define el propósito del ambiente al que pertenece el servidor.

| Código | Descripción |
| :--- | :--- |
| `prd` | **Producción**: Ambiente principal para usuarios finales. |
| `dr` | **Disaster Recovery**: Ambiente de contingencia y recuperación. |
| `qa` | **QA / Pruebas**: Ambiente para pruebas de calidad y funcionales. |
| `dev` | **Desarrollo**: Ambiente para el equipo de desarrollo. |

---

### 3. Aplicación (APLICACION)

Identifica la aplicación o sistema principal que aloja el servidor.

| Código | Descripción |
| :--- | :--- |
| `clp` | **Calypso**: Aplicación principal del proyecto. |

---

### 4. Rol del Servidor (ROL)

Describe la función específica que cumple el servidor dentro de la arquitectura de la aplicación.

| Código | Descripción |
| :--- | :--- |
| `app` | **Servidor de Aplicación**: Procesa la lógica de negocio (equivale al `cb` en los nombres originales). |
| `bd` | **Base de Datos**: Servidor que aloja la base de datos. |
| `acm` | **Módulo de Componente de Aplicación**: Para componentes específicos de Calypso. |
| `web` | **Servidor Web**: Servidor para interfaces web o frontales. |

---

### 5. Ubicación (UBICACION)

Indica el centro de datos (datacenter) donde está físicamente alojado el servidor.

| Código | Descripción |
| :--- | :--- |
| `aco` | Datacenter Aconcagua |
| `lgv` | Datacenter Longovilo |

---

### 6. Secuencia (SECUENCIA)

Número de dos dígitos que identifica de forma única al servidor dentro de un grupo con las mismas características (ej: clúster).

| Código | Descripción |
| :--- | :--- |
| `01` | Primer servidor |
| `02` | Segundo servidor |
| `...` | etc. |

---

## Ejemplos de Uso

**Ejemplo 1: Servidor de Aplicación en Producción**

Se necesita crear el primer servidor de aplicación para Calypso en el ambiente de Producción, ubicado en Aconcagua.
- **OS**: `lnx`
- **Entorno**: `prd`
- **Aplicación**: `clp`
- **Rol**: `app`
- **Ubicación**: `aco`
- **Secuencia**: `01`

**Nombre resultante:** `lnx-prd-clp-app-aco-01`

**Ejemplo 2: Servidor de Base de Datos en Disaster Recovery**

Se necesita crear el segundo servidor de base de datos para Calypso en el ambiente de Disaster Recovery, ubicado en Longovilo.
- **OS**: `lnx`
- **Entorno**: `dr`
- **Aplicación**: `clp`
- **Rol**: `bd`
- **Ubicación**: `lgv`
- **Secuencia**: `02`

**Nombre resultante:** `lnx-dr-clp-bd-lgv-02`
