import sys
from pathlib import Path
import pandas as pd

from scripts.procesamiento.rutas import obtener_ruta_relativa

# =====================================================================
# CONSTANTES DE CONFIGURACIÓN Y LOGGING
# =====================================================================
CARPETA_DEFAULT = "datos"

# Prefijos para el formateo de mensajes por consola
LOG_DEBUG = "[DEBUG]: "
LOG_ERROR = "[ERROR]: "

def cargar_csv(nombre_archivo, carpeta_origen=CARPETA_DEFAULT):
    """
    Lee un archivo CSV utilizando una ruta puramente relativa.
    Maneja excepciones en caso de que el archivo no sea encontrado o esté corrupto.
    """
    # Generamos la ruta relativa pura
    ruta_relativa = obtener_ruta_relativa(carpeta_origen, nombre_archivo)

    print(f"{LOG_DEBUG}Intentando abrir el archivo mediante ruta relativa: '{ruta_relativa}'")

    try:
        # Pandas recibe la ruta relativa y busca desde el directorio de ejecución
        df = pd.read_csv(ruta_relativa)
        print(f"{LOG_DEBUG}Archivo leído correctamente usando rutas relativas.")
        return df

    except FileNotFoundError:
        print(f"\n{LOG_ERROR}No se encontró el archivo en la ruta relativa: '{ruta_relativa}'")
        return None

    except Exception as e:
        print(f"\n{LOG_ERROR}Ocurrió un error inesperado al leer el archivo: {e}")
        return None
