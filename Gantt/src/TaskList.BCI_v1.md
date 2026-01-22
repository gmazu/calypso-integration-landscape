Perfecto. Versión **actualizada y limpia** de **las actividades que se deben agregar o ajustar en la Gantt de SixManager**, **solo lo que agregamos o movimos**, agrupado por **ID existente de la Gantt**, sin inventar IDs.

---

VERSIÓN
Gantt Calypso – Ajustes y agregados consensuados
Versión: V1.3
Ámbito: SixManager / BCI – Preproducción

---

ID 6 – Habilitación de infraestructura física (Pre requisitos)
**Posición:** Todas **al inicio** del ID 6 (sin dependencias)

Agregar actividades:

* Llenado formulario de Housing
* Llenado formulario de solicitud de IPs
* Llenado formulario de solicitud de Storage
* Llenado formulario de usuarios para accesos VPN

  * nombre
  * usuario
  * email
  * usuario corto
  * IP origen
  * IP destino
  * puertos
* Llenado formulario de acceso a GIT
* Recepción asignación de rack (ACO / LGV)
* Recepción asignación de IPs
* Solicitud de accesos VPN (con IPs ya asignadas)
* Construcción de script de pruebas de conectividad

  * input: IP destino + puertos (desde firewall)
* Ejecución de pruebas de conectividad

  * validación de IPs y puertos
  * evidencia de accesos OK / NOK

---

ID 21 – Prerrequisitos
**Posición:** Todo **al inicio del proyecto**, en paralelo a ID 6

Agregar actividades:

* Recepción / levantamiento ACIS Calypso
* Solicitud y recepción arquitectura TO-BE
* Definición de prerrequisitos Banco (TI + Negocio), checklist único:

  * Active Directory

    * IPs, cuentas, integraciones
  * Monitoreo

    * Nagios
    * Dynatrace
    * Grafana
  * Observabilidad
  * Backup (si aplica)
  * Cuentas técnicas / cuentas genéricas del proyecto
  * Accesos y condiciones de seguridad
  * Validación de riesgo y seguridad
* Definición de KPIs de negocio para monitoreo aplicativo
* Definición de plan de escalamiento

  * quién monitorea
  * quién atiende
  * a quién se escala
* Validación de criterios de recepción futura (preproductivo y productivo)

---

ID 29 – Habilitación OLVM
**Posición:** Al final del ID 29, antes de cerrarlo

Agregar actividad:

* Integración de OLVM con monitoreo Banco
* Re-ejecución de pruebas técnicas post-monitoreo (doble validación)

---

ID 37 – Habilitación Cluster OpenShift Preproductivo
**Posición:** Al final del ID 37

Agregar actividad:

* Integración de OpenShift con monitoreo Banco
* Re-ejecución de pruebas post-monitoreo
* Confirmación de no impacto del monitoreo

---

ID 45 – Habilitación BBDD
**Posición:** Al final del ID 45

Agregar actividades:

* Integración BBDD con monitoreo Banco
* Integración BBDD con respaldos (si aplica)
* Validación post-monitoreo

---

ID 51 – Despliegue y migración de aplicaciones DEV / UAT / INT
**Condición previa obligatoria (no al final):**

* Monitoreo técnico y aplicativo **ya definido, operativo y validado**
* Dashboards TI y Negocio listos antes de migrar

(No se agregan tareas nuevas aquí, se **condiciona el inicio**)

---

ID 59 – Integración de componentes
**Ajuste de orden (no se agregan tareas nuevas):**

* La actividad **ID 61 – Integración con Observabilidad y monitoreo**
  se ejecuta **dentro de cada etapa técnica**
  (OLVM, OpenShift, BBDD, Apps)
* No queda concentrada al final

---

ID 63 – Despliegue de aplicaciones en GIT
**Dependencia agregada:**

* Requiere **formulario de acceso a GIT gestionado en ID 6**

(No se agrega tarea aquí, se refuerza dependencia)

---

Si quieres, el siguiente paso natural es:

* convertir esto en **bloques listos para insertar por fila exacta**,
  o
* preparar el **README final V1.0** para adjuntar al proyecto.

