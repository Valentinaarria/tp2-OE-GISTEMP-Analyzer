import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

from .carga_de_datos import cargar_csv
from .rutas import obtener_ruta_relativa

# ==========================================
# MÓDULOS DE ANÁLISIS Y VISUALIZACIÓN
# ==========================================

def generar_csv(df, nombre_archivo, carpeta_destino):
    """Genera un archivo CSV en la carpeta de resultados."""
    ruta_csv = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    df.to_csv(ruta_csv, index=False)


def generar_grafico_barras(df, titulo, nombre_archivo, carpeta_destino, xValue, yValue, xLabel, yLabel, color, edge):
    """Genera un gráfico de barras en la carpeta de resultados."""
    plt.figure(figsize=(8, 5))
    plt.bar(df[xValue].astype(str), df[yValue], color=color, edgecolor=edge)
    plt.title(titulo, fontsize=14)
    plt.xlabel(xLabel, fontsize=12)
    plt.ylabel(yLabel, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    ruta_grafico = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    plt.savefig(ruta_grafico, bbox_inches='tight')
    plt.close()


def generar_grafico_lineal(df, titulo, nombre_archivo, carpeta_destino, xValue, yValue,color):
    """Genera un gráfico lineal en la carpeta de resultados."""
    plt.figure(figsize=(10, 5))
    plt.plot(df[xValue].astype(str), df[yValue], marker='o', color=color, linewidth=2, markersize=8)
    plt.title(titulo, fontsize=14)
    plt.xlabel('Década', fontsize=12)
    plt.ylabel('Promedio de Anomalía (°C)', fontsize=12)
    plt.grid(True, alpha=0.4)

    plt.fill_between(df[xValue].astype(str), df[yValue], color=color, alpha=0.1)

    ruta_grafico = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    plt.savefig(ruta_grafico, bbox_inches='tight')
    plt.close()


def generar_grafico_tendencia(df, titulo, nombre_archivo, carpeta_destino, xValue, yValue_base, yValue_tendencia):
    """Genera un gráfico comparativo de tendencia (datos anuales vs media móvil)."""
    plt.figure(figsize=(10, 6))

    # 1. Línea de datos anuales (suave/gris)
    plt.plot(df[xValue], df[yValue_base], label='Anomalía Anual', color='lightgrey', marker='.', alpha=0.7)

    # 2. Línea de la media móvil (destacada/roja)
    plt.plot(df[xValue], df[yValue_tendencia], label='Tendencia (10 años)', color='red', linewidth=2.5)

    # 3. Línea horizontal de referencia en 0
    plt.axhline(0, color='blue', linestyle='--', linewidth=1, label='Promedio Histórico Base')

    # Configuración de etiquetas y diseño
    plt.title(titulo, fontsize=14)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Anomalía de Temperatura (°C)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Guardar gráfico
    ruta_grafico = obtener_ruta_relativa(carpeta_destino, nombre_archivo)
    plt.savefig(ruta_grafico, bbox_inches='tight')
    plt.close()

# ==========================================
# MÓDULOS DE ANÁLISIS
# ==========================================

def procesar_top5(df):
    """Calcula el Top 5 meses mas calurosos."""
    print("Procesando Top 5 años más calurosos.")
    return df.sort_values(by='Mean', ascending=False).head(5)


def procesar_decadas(df):
    """Agrupa por décadas y muestra la evolucion climatica."""
    print("Procesando evolución por décadas.")
    df_temp = df.copy()
    df_temp['Year'] = df_temp['Year'].astype(int)
    df_temp['Decade'] = (df_temp['Year'] // 10) * 10
    return df_temp.groupby('Decade')['Mean'].mean().reset_index()


def procesar_tendencia(df):
    """Calcula la media móvil, para generar datos de tendencia historica."""
    print("Procesando tendencia histórica (Media Móvil).")
    df_tendencia = df.sort_values('Year').copy()
    df_tendencia['Rolling_Mean'] = df_tendencia['Mean'].rolling(window=10).mean()
    return df_tendencia


def procesar_estacionalidad_mensual(df):
    """Analiza los datos mensuales: separa año/mes."""
    print("Procesando estacionalidad mensual.")
    df_temp = df.copy()
    df_temp[['Anio', 'Mes']] = df_temp['Year'].str.split('-', expand=True)
    return df_temp.groupby('Mes')['Mean'].mean().reset_index()


def main():

    print("Iniciando programa de análisis climático...\n")
    print("Preparacion...\n")

    carpeta_resultados = "resultados"

    # 1. Cargar ambos datasets usando el módulo de carga
    try:
        df_anual = cargar_csv('annual.csv')
        df_mensual = cargar_csv('monthly.csv')
        
    except FileNotFoundError as e:
        print(f"\n[ERROR]: No se encontró uno de los archivos necesarios para el análisis.")
        return 
        
    except Exception as e:
        print(f"\n[ERROR]: Ocurrió un fallo inesperado al procesar los archivos (archivo vacío o corrupto).")
        return

    # 2. Filtrar ambos DataFrames por la agencia GISTEMP
    df_agencia_anual = df_anual[df_anual['Source'] == 'GISTEMP']
    df_agencia_mensual = df_mensual[df_mensual['Source'] == 'GISTEMP'] # FILTRO MENSUAL

    print("Iniciando análisis...\n")

    # 1. Análisis Anual
    print("\n--- ANÁLISIS ANUAL ---")
    top5 = procesar_top5(df_agencia_anual)

    #Resultados del analisis anual
    generar_csv(top5[['Year', 'Mean']], '01_top5_anuales.csv', carpeta_resultados)
    generar_grafico_barras(top5, 'Top 5 Años con Mayor Anomalía Térmica', '01_grafico_top5.png', carpeta_resultados, 'Year', 'Mean', 'Año', 'Anomalía Promedio (°C)','darkorange', 'black')

    #2. Analisis por decada
    decadas = procesar_decadas(df_agencia_anual)

    #Resultados decadas
    generar_csv(decadas, '02_decadas.csv', carpeta_resultados)
    generar_grafico_lineal(decadas, 'Evolución de la Temperatura por Décadas', '02_grafico_decadas.png', carpeta_resultados, 'Decade', 'Mean', 'purple')

    #3. Analisis de tendencia climatica
    df_tendencia = procesar_tendencia(df_agencia_anual)

    #Resultados Tendencia
    df_export = df_tendencia[['Year', 'Mean', 'Rolling_Mean']].dropna()
    generar_csv(df_export, '03_tendencia_historica.csv', carpeta_resultados)
    generar_grafico_tendencia(df_tendencia, 'Tendencia Histórica de Temperatura', '03_grafico_tendencia.png', carpeta_resultados, 'Year', 'Mean', 'Rolling_Mean')

    #4. Análisis Mensual
    print("\n--- ANÁLISIS MENSUAL ---")
    promedio_mensual = procesar_estacionalidad_mensual(df_agencia_mensual)

    #Resultados promedios mensuales
    generar_csv(promedio_mensual, '05_promedio_por_mes.csv', carpeta_resultados)

    #Meses para el grafico
    promedio_mensual['Nombre_Mes'] = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    generar_grafico_barras(
        promedio_mensual,
        'Anomalía Térmica Promedio por Mes (Histórico)',
        '05_grafico_estacionalidad.png',
        carpeta_resultados,
        'Nombre_Mes',
        'Mean',
        'Mes del Año',
        'Anomalía Promedio (°C)',
        'teal',
        'black'
    )

    print("[SUCCESS] Se han generado múltiples archivos .csv y gráficos .png.")


main()
