# GISTEMP-Analyzer 🌍🌡️

## Descripción del Proyecto
Este proyecto de programación en Python está diseñado para el procesamiento, análisis y visualización de registros históricos de temperatura a nivel mundial. El objetivo principal es transformar datos climáticos puros en información estratégica que permita identificar y comprender las tendencias del calentamiento global a lo largo del tiempo.

---

## 👥 Integrantes del Equipo
* **Hugo** - Líder Técnico (Technical Lead)
* **Paco** - Desarrollador (Developer)
* **Luis** - Control de Calidad (QA)

---

## 📊 Escenario Elegido: Datos Climáticos Globales
Para este análisis se seleccionó un escenario enfocado en el cambio climático global, utilizando series temporales que son un estándar en la investigación científica y la educación.

### Características del Dataset
* **Contenido:** Datos de temperatura promedio global.
* **Frecuencia:** Registros detallados de manera mensual y anual.
* **Formato:** Archivo de texto plano separado por comas (`.csv`).
* **Origen:** El dataset versionado en este proyecto consolida registros climáticos provenientes de dos fuentes oficiales y de referencia global:
1.  **GISTEMP** (NASA Goddard Institute for Space Studies): Enfocado en las anomalías de la temperatura superficial global utilizando como período base los años 1951-1980.
2.  **GCAG** (Global Climate Anomalies / UK Met Office HadCRUT5 / NOAA GlobalTemp): Provee estimaciones consolidadas de anomalías térmicas relativas al promedio global del siglo XX.

Ambas fuentes conviven dentro de la estructura de archivos y están correctamente tipificadas en el Diccionario de Datos para garantizar un análisis comparativo robusto.

### 🌐 Acceso al Dataset
El dataset original se encuentra disponible y actualizado de forma pública en:
🔗 [DataHub.io - Global Temperature](https://datahub.io/core/global-temp)

## 📊 Diccionario de Datos

El sistema procesa archivos de anomalías de temperatura global con la siguiente estructura de campos:

- annual.csv

| Field | Type | Description |
| :--- | :--- | :--- |
| **Source** | string | Data provider identifier: GISTEMP (NASA Goddard Institute for Space Studies) or GCAG (UK Met Office HadCRUT5). |
| **Year** | year | YYYY |
| **Mean** | number | Average global mean temperature anomalies in degrees Celsius relative to a base period. GISTEMP base period: 1951-1980. GCAG base period: 20th century average. |
---

-  monthly.csv

| Field | Type | Description |
| :--- | :--- | :--- |
| **Source** | string | Data provider identifier: GISTEMP (NASA Goddard Institute for Space Studies) or GCAG (UK Met Office HadCRUT5). |
| **Year** |  date (YYYY-MM) | YYYY-MM |
| **Mean** | number | Average global mean temperature anomalies in degrees Celsius relative to a base period. GISTEMP base period: 1951-1980. GCAG base period: 20th century average. |
---


## 🚀 Instrucciones de Ejecución Básicas
Para clonar este proyecto en tu entorno local, ejecutá los siguientes comandos en tu terminal:

    # 1. Clonar el repositorio
    git clone https://github.com/Valentinaarria/tp2-OE-GISTEMP-Analyzer.git

    # 2. Ingresar a la carpeta del proyecto
    cd tp2-OE-GISTEMP-Analyzer
