# GISTEMP-Analyzer

## Descripción del Proyecto
Este proyecto de programación en Python está diseñado para el procesamiento, análisis y visualización de registros históricos de temperatura a nivel mundial. El objetivo principal es transformar datos climáticos puros en información estratégica que permita identificar y comprender las tendencias del calentamiento global a lo largo del tiempo.

## Integrantes del Equipo
* Hugo - Líder Técnico (Technical Lead)
* Paco - Desarrollador (Developer)
* Luis - Control de Calidad (QA)

---

## Estructura del Repositorio

Para facilitar la navegación y asegurar la modularidad del código, el proyecto está organizado de la siguiente manera:
``` text
tp2-OE-GISTEMP-Analyzer/
├── datos/                             # Archivos CSV crudos de entrada
│   ├── annual.csv
│   └── monthly.csv
├── resultados/                        # Reportes y gráficos generados por el script
├── scripts/
│   ├── __init__.py
│   ├── procesamiento/                 # Módulos de lógica de negocio y utilitarios
│   │   ├── __init__.py
│   │   ├── analizador.py              # Pipeline principal y lógica de análisis
│   │   ├── carga_de_datos.py          # Lógica de lectura de archivos
│   │   └── rutas.py                   # Gestión automatizada de rutas relativas
│   └── tests/                         # Suite de pruebas unitarias (Unittest)
│       ├── __init__.py
│       ├── test_carga_datos.py        # Pruebas de IO y excepciones de carga
│       ├── test_exportaciones.py      # Pruebas de velocidad, renderizado PNG y IO
│       └── test_procesamiento.py      # Pruebas de cálculos matemáticos y Pandas
├── README.md                          # Documentación del proyecto
└── requirements.txt                   # Archivo de dependencias de terceros
```
---

##  Arquitectura y Flujo de Datos
El software está diseñado bajo un enfoque modular, dividiendo las responsabilidades de IO (Entrada/Salida), procesamiento lógico y visualización:

1. Fase de Carga (IO): El script carga_de_datos.py localiza los archivos en la carpeta datos/ utilizando el asistente de rutas.py para asegurar compatibilidad de separadores de directorios (/ o \\) entre Windows, Linux y macOS.
2. Fase de Filtrado y Transformación: analizador.py toma los DataFrames en memoria, aísla los registros correspondientes a la agencia configurada (GISTEMP) y ejecuta las funciones matemáticas agregadas (ordenamiento, promedios móviles con .rolling() y agrupamientos con .groupby()).
3. Fase de Exportación: Las funciones de visualización procesan las matrices de datos y, utilizando el backend no interactivo Agg de Matplotlib, escriben de forma directa y silenciosa los reportes .csv y las imágenes .png en la carpeta resultados/.

---

## Escenario Elegido: Datos Climáticos Globales
Para este análisis se seleccionó un escenario enfocado en el cambio climático global, utilizando series temporales que son un estándar en la investigación científica y la educación.

### Características del Dataset
* **Contenido:** Datos de temperatura promedio global.
* **Frecuencia:** Registros detallados de manera mensual y anual.
* **Formato:** Archivo de texto plano separado por comas (`.csv`).
* **Origen:** Dataset público de temperatura global disponible en DataHub, cuya columna `Source` puede incluir series como `GISTEMP` (NASA Goddard Institute for Space Studies) y `GCAG`; en este proyecto, el análisis se realiza filtrando la fuente **GISTEMP**.

### Acceso al Dataset
El dataset original se encuentra disponible y actualizado de forma pública en:
🔗 [DataHub.io - Global Temperature](https://datahub.io/core/global-temp)

##  Diccionario de Datos

El sistema procesa archivos de anomalías de temperatura global con la siguiente estructura de campos:

- annual.csv

| Field | Type | Description |
| :--- | :--- | :--- |
| **Source** | string | Data provider identifier: GISTEMP (NASA Goddard Institute for Space Studies) or GCAG (UK Met Office HadCRUT5). |
| **Year** | year | YYYY |
| **Mean** | number | Average global mean temperature anomalies in degrees Celsius relative to a base period. GISTEMP base period: 1951-1980. GCAG base period: 20th century average. |
---

 - monthly.csv

| Field | Type | Description |
| :--- | :--- | :--- |
| **Source** | string | Data provider identifier: GISTEMP (NASA Goddard Institute for Space Studies) or GCAG (UK Met Office HadCRUT5). |
| **Year** | date(YYYY-MM) | YYYY-MM |
| **Mean** | number | Average global mean temperature anomalies in degrees Celsius relative to a base period. GISTEMP base period: 1951-1980. GCAG base period: 20th century average. |
---

---

## Prerrequisitos y Librerías

El proyecto requiere Python 3.10 o superior y las siguientes librerías de terceros:
* Pandas: Para la manipulación, filtrado y análisis de las series temporales.
* Matplotlib: Para la generación y renderizado de gráficos estadísticos en formato PNG.

> Nota: Si ejecutás este proyecto dentro de un entorno de Google Colab, estas librerías ya vienen instaladas por defecto de fábrica. Si estás corriendo el proyecto de forma local en una computadora limpia o un servidor CI, recordá instalarlas antes de comenzar.

### Instalación de dependencias:
Asegurate de estar situado en la raíz del repositorio y ejecutá en la terminal:

```sh
pip install -r requirements.txt
```

## Instrucciones de Ejecución

Para correr el proyecto (sea en tu entorno local o en las celdas de Google Colab), seguí estos pasos de forma ordenada.

### 1. Preparar el entorno (Clonar e ingresar)
```sh
# Clonar el repositorio
git clone https://github.com/Valentinaarria/tp2-OE-GISTEMP-Analyzer.git

# Ingresar a la carpeta del proyecto
cd tp2-OE-GISTEMP-Analyzer
```
*(Si estás trabajando en Google Colab, recordá anteponer el signo % para que el cambio de directorio sea permanente entre celdas: %cd tp2-OE-GISTEMP-Analyzer)*

### 2. Ejecutar el Analizador Principal
Para correr el pipeline de procesamiento de datos y generación de gráficos, ejecutá el módulo como un script ejecutable desde la raíz del proyecto:
python -m scripts.procesamiento.analizador

#### 📊 Resultado Esperado de la Ejecución
Al correr el programa, verás el progreso paso a paso detallado en la consola:

```text
Iniciando programa de analisis climatico...

Preparacion...

[DEBUG]: Intentando abrir el archivo mediante ruta relativa: 'datos/annual.csv'
[DEBUG]: Archivo leido correctamente usando rutas relativas.
[DEBUG]: Intentando abrir el archivo mediante ruta relativa: 'datos/monthly.csv'
[DEBUG]: Archivo leido correctamente usando rutas relativas.
Iniciando analisis...


--- ANÁLISIS ANUAL ---
Procesando Top 5 anos mas calurosos.
Procesando evolucion por decadas.
Procesando tendencia historica (Media Movil).

--- ANÁLISIS MENSUAL ---
Procesando estacionalidad mensual.

[SUCCESS] Se han generado multiples archivos .csv y graficos .png.

```

Una vez finalizado el script, se creará automáticamente una carpeta llamada resultados/ en la raíz del repositorio que contendrá los siguientes elementos:
* 01_top5_anuales.csv y 01_grafico_top5.png: Datos y gráfico de barras naranja que destaca los 5 años con mayores anomalías térmicas globales.
* 02_decadas.csv y 02_grafico_decadas.png: Gráfico lineal púrpura con área sombreada que detalla la evolución promedio calculada por décadas.
* 03_tendencia_historica.csv y 03_grafico_tendencia.png: Gráfico de líneas que cruza la fluctuación de anomalías de cada año frente a la línea roja de tendencia por media móvil (ventana de 10 años).
* 05_promedio_por_mes.csv y 05_grafico_estacionalidad.png: Gráfico de barras color teal que expone el comportamiento estacional medio de cada mes del año de forma histórica.

---

## Robustez y Manejo de Errores
El sistema implementa bloques try-except de control de flujo en su punto de entrada principal para evitar interrupciones abruptas críticas (crashes):
* FileNotFoundError: Captura la ausencia física de los archivos fuente de datos (como annual.csv o monthly.csv), notificando al usuario la falta de un archivo requerido mediante un mensaje amigable en consola en lugar de lanzar un Traceback complejo.
* Exception (Genérica): Resguarda el flujo ante cualquier anomalía imprevista de los datos, tales como archivos dañados, vacíos o con problemas de codificación, cerrando la ejecución del script de manera segura.

---

## Suite de Pruebas Unitarias (Testing)

El proyecto cuenta con una sólida cobertura de pruebas automatizadas que aseguran el correcto funcionamiento de los cálculos lógicos y la persistencia en disco. Están diseñadas para ejecutarse de manera limpia tanto localmente como en entornos de Integración Continua (CI) sin interfaz gráfica (Headless) gracias a la configuración del backend no interactivo Agg de Matplotlib.

### Pruebas Disponibles en el Repositorio:
1. TestCargaYRutado (test_carga_datos.py): Valida la construcción de rutas relativas sin importar el Sistema Operativo, la lectura exitosa de archivos CSV hacia estructuras DataFrame de Pandas y el lanzamiento controlado de excepciones FileNotFoundError.
2. TestProcesamientoDatos (test_procesamiento.py): Asegura la fidelidad matemática de las funciones de negocio: ordenamiento del Top 5, agrupamientos promedio por décadas, ventanas móviles de tendencia y segmentación mensual estacional.
3. TestExportaciones (test_exportaciones.py): Verifica que los reportes de datos se escriban correctamente en disco y que Matplotlib logre renderizar y guardar de forma segura los archivos PNG sin bloquear la consola ni generar logs ruidosos innecesarios.

### Cómo ejecutar los tests:
Para lanzar la suite completa en modo detallado (verbose) y verificar que todas las aserciones pasen en verde de manera limpia y silenciosa, ejecutá desde la raíz:
```sh
python -m unittest discover -s scripts/tests -t . -v
```
