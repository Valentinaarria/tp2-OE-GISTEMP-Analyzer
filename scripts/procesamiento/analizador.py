import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

# Detectamos la raíz:
directorio_raiz = str(Path(__file__).resolve().parent.parent.parent)

if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

os.chdir(directorio_raiz)

from scripts.procesamiento.carga_de_datos import cargar_csv
from scripts.procesamiento.rutas import obtener_ruta_relativa

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

    # 1. Separar la columna 'Year' (que viene como 'YYYY-MM') en 'Anio' y 'Mes'
    # expand=True divide el string en dos columnas distintas
    df_temp[['Anio', 'Mes']] = df_temp['Year'].str.split('-', expand=True)

    # ANÁLISIS A: Top 5 Meses Individuales
    top5_meses = df_temp.sort_values(by='Mean', ascending=False).head(5)


    # ANÁLISIS B: Promedio de Anomalía por Mes
    # Agrupamos por mes ('01', '02', etc.) y calculamos la media histórica
    return  df_temp.groupby('Mes')['Mean'].mean().reset_index()


def main():
    
    directorio_raiz = Path(__file__).resolve().parent.parent.parent

    os.chdir(directorio_raiz)

    print(f"Directorio de trabajo ajustado automáticamente a: {os.getcwd()}")

    print("Iniciando análisis climático...\n")

    # 1. Cargar ambos datasets usando el módulo de carga
    df_anual = cargar_csv('annual.csv')
    df_mensual = cargar_csv('monthly.csv')

    if df_anual is None or df_mensual is None:
        print("[ERROR]: No se pudieron cargar los datos. Abortando análisis.")
        return

    # 3. Filtrar ambos DataFrames por la agencia GISTEMP
    df_agencia_anual = df_anual[df_anual['Source'] == 'GISTEMP']
    df_agencia_mensual = df_mensual[df_mensual['Source'] == 'GISTEMP'] # FILTRO MENSUAL

    # 4. Ejecutar el pipeline de análisis Anual
    print("\n--- ANÁLISIS ANUAL ---")
    print(procesar_top5(df_agencia_anual))
    print(procesar_decadas(df_agencia_anual))
    print(procesar_tendencia(df_agencia_anual))

    # 5. Ejecutar el pipeline de análisis Mensual
    print("\n--- ANÁLISIS MENSUAL ---")
    print(procesar_estacionalidad_mensual(df_agencia_mensual))


if __name__ == "__main__":
    main()
