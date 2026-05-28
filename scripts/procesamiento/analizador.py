"""
Modulo principal de analisis climatico y visualizacion de anomalias termicas.
Procesa datos anuales y mensuales generando reportes CSV y graficos PNG.
"""

import matplotlib as plt
plt.use('Agg')
import os

from .carga_de_datos import cargar_csv
from .rutas import obtener_ruta_relativa

# ==========================================
# CONSTANTES CONFIGURABLES 
# ==========================================
CARPETA_RESULTADOS = 'resultados'
AGENCIA_FILTRO = 'GISTEMP'

# Archivos de entrada
CSV_ENTRADA_ANUAL = 'annual.csv'
CSV_ENTRADA_MENSUAL = 'monthly.csv'

# Estructura de datos (Columnas de los DataFrames)
COL_YEAR = 'Year'
COL_MEAN = 'Mean'
COL_SOURCE = 'Source'
COL_DECADE = 'Decade'
COL_ROLLING = 'Rolling_Mean'
COL_ANIO_PROP = 'Anio'
COL_MES_PROP = 'Mes'
COL_LABEL_MES = 'Nombre_Mes'

# Parametros de procesamiento
CANTIDAD_TOP_ANIOS = 5
VENTANA_MEDIA_MOVIL = 10

# Nombres de los meses mapeados
NOMBRES_MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

# Archivos de salida (Reportes y Graficos)
CSV_TOP5 = '01_top5_anuales.csv'
PNG_TOP5 = '01_grafico_top5.png'
CSV_DECADAS = '02_decadas.csv'
PNG_DECADAS = '02_grafico_decadas.png'
CSV_TENDENCIA = '03_tendencia_historica.csv'
PNG_TENDENCIA = '03_grafico_tendencia.png'
CSV_MENSUAL = '05_promedio_por_mes.csv'
PNG_MENSUAL = '05_grafico_estacionalidad.png'

# Titulos y etiquetas esteticas de graficos
TITULO_TOP5 = 'Top 5 Anios con Mayor Anomalia Termica'
TITULO_DECADAS = 'Evolucion de la Temperatura por Decadas'
TITULO_TENDENCIA = 'Tendencia Historica de Temperatura'
TITULO_MENSUAL = 'Anomalia Termica Promedio por Mes (Historico)'

# ==========================================
# MÓDULOS DE ANÁLISIS Y VISUALIZACIÓN
# ==========================================

def generar_csv(df, nombre_archivo, carpeta_destino):
    """
    Genera un archivo CSV en la carpeta de resultados especificada.
    """
    ruta_csv = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    df.to_csv(ruta_csv, index=False)


def generar_grafico_barras(df, titulo, nombre_archivo, carpeta_destino, xValue, yValue, xLabel, yLabel, color, edge):
    """
    Genera un grafico de barras y lo exporta a la carpeta de resultados como PNG.
    """
    plt.figure(figsize=(8, 5))
    plt.bar(df[xValue].astype(str), df[yValue], color=color, edgecolor=edge)
    plt.title(titulo, fontsize=14)
    plt.xlabel(xLabel, fontsize=12)
    plt.ylabel(yLabel, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    ruta_grafico = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    plt.savefig(ruta_grafico, bbox_inches='tight')
    plt.close()


def generar_grafico_lineal(df, titulo, nombre_archivo, carpeta_destino, xValue, yValue, color):
    """
    Genera un grafico lineal de evolucion temporal con sombreado de relleno.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(df[xValue].astype(str), df[yValue], marker='o', color=color, linewidth=2, markersize=8)
    plt.title(titulo, fontsize=14)
    plt.xlabel('Decada', fontsize=12)
    plt.ylabel('Promedio de Anomalia (C)', fontsize=12)
    plt.grid(True, alpha=0.4)

    plt.fill_between(df[xValue].astype(str), df[yValue], color=color, alpha=0.1)

    ruta_grafico = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    plt.savefig(ruta_grafico, bbox_inches='tight')
    plt.close()


def generar_grafico_tendencia(df, titulo, nombre_archivo, carpeta_destino, xValue, yValue_base, yValue_tendencia):
    """
    Genera un grafico comparativo cruzando los datos anuales con la media movil filtrada.
    """
    plt.figure(figsize=(10, 6))

    plt.plot(df[xValue], df[yValue_base], label='Anomalia Anual', color='lightgrey', marker='.', alpha=0.7)
    plt.plot(df[xValue], df[yValue_tendencia], label=f'Tendencia ({VENTANA_MEDIA_MOVIL} anios)', color='red', linewidth=2.5)
    plt.axhline(0, color='blue', linestyle='--', linewidth=1, label='Promedio Historico Base')

    plt.title(titulo, fontsize=14)
    plt.xlabel('Anio', fontsize=12)
    plt.ylabel('Anomalia de Temperatura (C)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)

    ruta_grafico = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    plt.savefig(ruta_grafico, bbox_inches='tight')
    plt.close()

# ==========================================
# MÓDULOS DE ANÁLISIS
# ==========================================

def procesar_top5(df):
    """
    Calcula los N periodos mas calurosos del set de datos ordenados de mayor a menor.
    """
    print(f"Procesando Top {CANTIDAD_TOP_ANIOS} anos mas calurosos.")
    return df.sort_values(by=COL_MEAN, ascending=False).head(CANTIDAD_TOP_ANIOS)


def procesar_decadas(df):
    """
    Agrupa cronologicamente las observaciones por decadas calculando sus medias.
    """
    print("Procesando evolucion por decadas.")
    df_temp = df.copy()
    df_temp[COL_YEAR] = df_temp[COL_YEAR].astype(int)
    df_temp[COL_DECADE] = (df_temp[COL_YEAR] // 10) * 10
    return df_temp.groupby(COL_DECADE)[COL_MEAN].mean().reset_index()


def procesar_tendencia(df):
    """
    Calcula la media movil (ventana configurable) para suavizar tendencias historicas.
    """
    print("Procesando tendencia historica (Media Movil).")
    df_tendencia = df.sort_values(COL_YEAR).copy()
    df_tendencia[COL_ROLLING] = df_tendencia[COL_MEAN].rolling(window=VENTANA_MEDIA_MOVIL).mean()
    return df_tendencia


def procesar_estacionalidad_mensual(df):
    """
    Segmenta las fechas mensuales para agrupar y promediar las anomalias estacionales.
    """
    print("Procesando estacionalidad mensual.")
    df_temp = df.copy()
    df_temp[[COL_ANIO_PROP, COL_MES_PROP]] = df_temp[COL_YEAR].str.split('-', expand=True)
    return df_temp.groupby(COL_MES_PROP)[COL_MEAN].mean().reset_index()


def main():
    """
    Flujo principal de ejecucion del pipeline de analisis climatico.
    """
    print("Iniciando programa de analisis climatico...\n")
    print("Preparacion...\n")

    # 1. Cargar ambos datasets mapeando errores de forma explicita
    try:
        df_anual = cargar_csv(CSV_ENTRADA_ANUAL)
        df_mensual = cargar_csv(CSV_ENTRADA_MENSUAL)
    except FileNotFoundError as e:
        print(f"\n[ERROR]: No se encontro uno de los archivos necesarios para el analisis.")
        return 
    except Exception as e:
        print(f"\n[ERROR]: Ocurrio un fallo inesperado al procesar los archivos (archivo vacio o corrupto).")
        return

    # 2. Asegurar existencia de la carpeta resultados
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    # 3. Filtrar ambos DataFrames por la agencia seleccionada
    df_agencia_anual = df_anual[df_anual[COL_SOURCE] == AGENCIA_FILTRO]
    df_agencia_mensual = df_mensual[df_mensual[COL_SOURCE] == AGENCIA_FILTRO]

    print("Iniciando analisis...\n")

    # --- ANÁLISIS ANUAL ---
    print("\n--- ANÁLISIS ANUAL ---")
    top5 = procesar_top5(df_agencia_anual)

    generar_csv(top5[[COL_YEAR, COL_MEAN]], CSV_TOP5, CARPETA_RESULTADOS)
    generar_grafico_barras(top5, TITULO_TOP5, PNG_TOP5, CARPETA_RESULTADOS, COL_YEAR, COL_MEAN, 'Ano', 'Anomalia Promedio (C)', 'darkorange', 'black')

    # --- ANÁLISIS POR DÉCADA ---
    decadas = procesar_decadas(df_agencia_anual)

    generar_csv(decadas, CSV_DECADAS, CARPETA_RESULTADOS)
    generar_grafico_lineal(decadas, TITULO_DECADAS, PNG_DECADAS, CARPETA_RESULTADOS, COL_DECADE, COL_MEAN, 'purple')

    # --- ANÁLISIS DE TENDENCIA HISTÓRICA ---
    df_tendencia = procesar_tendencia(df_agencia_anual)

    df_export = df_tendencia[[COL_YEAR, COL_MEAN, COL_ROLLING]].dropna()
    generar_csv(df_export, CSV_TENDENCIA, CARPETA_RESULTADOS)
    generar_grafico_tendencia(df_tendencia, TITULO_TENDENCIA, PNG_TENDENCIA, CARPETA_RESULTADOS, COL_YEAR, COL_MEAN, COL_ROLLING)

    # --- ANÁLISIS MENSUAL ---
    print("\n--- ANÁLISIS MENSUAL ---")
    promedio_mensual = procesar_estacionalidad_mensual(df_agencia_mensual)

    generar_csv(promedio_mensual, CSV_MENSUAL, CARPETA_RESULTADOS)

  # Mapeo de nombres cortos para la etiqueta estacional a partir del valor de mes
     mes_a_nombre = {f"{i:02d}": nombre for i, nombre in enumerate(NOMBRES_MESES, start=1)}
     promedio_mensual[COL_LABEL_MES] = promedio_mensual[COL_MES_PROP].map(mes_a_nombre)


    generar_grafico_barras(
        promedio_mensual,
        TITULO_MENSUAL,
        PNG_MENSUAL,
        CARPETA_RESULTADOS,
        COL_LABEL_MES,
        COL_MEAN,
        'Mes del Ano',
        'Anomalia Promedio (C)',
        'teal',
        'black'
    )

    print("\n[SUCCESS] Se han generado multiples archivos .csv y graficos .png.")


if __name__ == "__main__":
    main()
