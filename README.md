# Calypso Integration Landscape (CLI)

---

## Descripción general

Calypso Integration Landscape (CLI) es un **proyecto de referencia conceptual y visual** que describe cómo la plataforma Calypso suele integrarse dentro del ecosistema tecnológico de una institución financiera.

Este repositorio se basa **exclusivamente en información pública** (brochures, whitepapers, presentaciones de producto y prácticas estándar de la industria).
No contiene código propietario, documentación confidencial, configuraciones reales de clientes ni detalles internos de implementación.

El objetivo es ofrecer una **visión clara, genérica y educativa** del rol de Calypso como plataforma front-to-back y de sus patrones de integración más comunes.

---

## Propósito

Este proyecto existe para:

* Visualizar la posición de Calypso dentro de una arquitectura típica de mercados financieros
* Representar los sistemas y servicios externos con los que Calypso suele integrarse
* Proveer un **modelo conceptual de integraciones** reutilizable
* Servir como material de apoyo para análisis, diseño y discusión técnica
* Permitir la generación de diagramas y animaciones (usando Manim) para documentación y presentaciones

Este proyecto **no es**:

* Una guía de despliegue productivo
* Una implementación real o funcional
* Ingeniería inversa de Calypso
* Documentación oficial del proveedor
* Arquitectura de un cliente específico

---

## Alcance

Incluido en el alcance:

* Diagramas lógicos de arquitectura
* Flujos conceptuales de integración
* Categorización de sistemas externos
* Servicios y plataformas conocidas públicamente
* Representaciones visuales estáticas y animadas

Explícitamente fuera de alcance:

* Infraestructura física o virtual
* Dimensionamiento, rendimiento o alta disponibilidad
* Esquemas de base de datos o componentes internos
* Nombres de clientes, ambientes o proyectos reales
* APIs propietarias o protocolos internos

---

## Arquitectura conceptual

A alto nivel, Calypso se representa como una **plataforma central front-to-back**, que se integra con distintos dominios externos, tales como:

* Proveedores de datos de mercado
* Plataformas de trading y brokers
* Redes de mensajería y pagos
* Sistemas de custodia, clearing y settlement
* Sistemas contables y core financiero
* Capas de seguridad, identidad e integración

Todas las representaciones son **lógicas y conceptuales**, no planos técnicos de implementación.

---

## Generación de diagramas

Este repositorio está pensado para soportar **generación de diagramas utilizando Manim**.

Manim se utiliza para:

* Crear diagramas de arquitectura claros y animados
* Mostrar flujos de datos e interacciones entre sistemas
* Construir activos visuales reutilizables

Las animaciones priorizan **claridad explicativa** por sobre efectos visuales.

---

## Estructura del repositorio (intención inicial)

* `/docs`
  Documentación conceptual y explicativa

* `/diagrams`
  Diagramas de arquitectura (estáticos o exportados)

* `/manim`
  Scripts Manim para diagramas animados

* `/assets`
  Imágenes y recursos visuales

(Esta estructura puede evolucionar con el proyecto.)

---

## Audiencia

Este proyecto está orientado a:

* Arquitectos de solución
* Ingenieros de plataforma
* Líderes técnicos
* Analistas de mercados financieros o tesorería
* Personas que necesiten entender Calypso a nivel conceptual

---

## Disclaimer

Este proyecto es **independiente y no oficial**.

* Calypso es una marca registrada de sus respectivos propietarios
* Este repositorio no está afiliado ni respaldado por el proveedor
* Todo el contenido proviene de información pública y conocimiento general de la industria
* Cualquier similitud con arquitecturas reales es coincidencia

---

## Estado del proyecto

Estado actual: **Conceptual / v0.x**

El proyecto avanza de forma incremental y con versionado conservador.

---

## Licencia

Este repositorio tiene fines **educativos y de referencia conceptual**.
La licencia open source se definirá una vez estabilizada la estructura.

