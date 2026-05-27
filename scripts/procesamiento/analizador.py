import pandas as pd

from scripts.procesamiento.carga_de_datos import cargar_csv

# ==========================================
# MÓDULOS DE ANÁLISIS
# ==========================================

def procesar_top5(df):
    """Calcula el Top 5 años más calurosos."""
    print("Procesando Top 5 años más calurosos.")
    return df.sort_values(by='Mean', ascending=False).head(5)

def procesar_decadas(df):
    """Agrupa por décadas y muestra la evolución climática."""
    print("Procesando evolución por décadas.")
    df_temp = df.copy()
    df_temp['Year'] = df_temp['Year'].astype(int)
    df_temp['Decade'] = (df_temp['Year'] // 10) * 10
    return df_temp.groupby('Decade')['Mean'].mean().reset_index()

def procesar_tendencia(df):
    """Calcula la media móvil para generar datos de tendencia histórica."""
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
    print("Iniciando análisis climático...\n")

    df_anual = cargar_csv('annual.csv')
    df_mensual = cargar_csv('monthly.csv')

    if df_anual is None or df_mensual is None:
        print("[ERROR]: No se pudieron cargar los datos. Abortando análisis.")
        return

    # 1. Filtrar ambos DataFrames por la agencia GISTEMP
    df_agencia_anual = df_anual[df_anual['Source'] == 'GISTEMP']
    df_agencia_mensual = df_mensual[df_mensual['Source'] == 'GISTEMP']

    # 2. Ejecutar el pipeline de análisis Anual
    print("\n--- ANÁLISIS ANUAL ---")
    print(procesar_top5(df_agencia_anual))
    print(procesar_decadas(df_agencia_anual))
    print(procesar_tendencia(df_agencia_anual))

    # 3. Ejecutar el pipeline de análisis Mensual
    print("\n--- ANÁLISIS MENSUAL ---")
    print(procesar_estacionalidad_mensual(df_agencia_mensual))


# Configuración segura del entorno requerida por el PR
if __name__ == "__main__":
    import sys
    import os
    from pathlib import Path

    directorio_raiz = Path(__file__).resolve().parent.parent.parent


    if str(directorio_raiz) not in sys.path:
        sys.path.insert(0, str(directorio_raiz))

    main()
