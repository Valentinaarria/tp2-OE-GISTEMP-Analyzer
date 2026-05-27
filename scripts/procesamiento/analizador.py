from .carga_de_datos import cargar_csv

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
    print("Iniciando análisis climático\n")

    try:
        df_anual = cargar_csv('annual.csv')
        df_mensual = cargar_csv('monthly.csv')
        
    except FileNotFoundError as e:
        print(f"\n[ERROR]: No se encontró uno de los archivos necesarios para el análisis.")
        return 
        
    except Exception as e:
        print(f"\n[ERROR]: Ocurrió un fallo inesperado al procesar los archivos (archivo vacío o corrupto).")
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


if __name__ == "__main__":
    main()
