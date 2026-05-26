import pandas as pd

from .rutas import obtener_ruta_relativa

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
    Maneja y re-lanza excepciones específicas si el archivo no existe,
    está vacío o tiene un formato corrupto.
    """
    # Generamos la ruta relativa pura
    ruta_relativa = obtener_ruta_relativa(carpeta_origen, nombre_archivo)

    print(f"{LOG_DEBUG}Intentando abrir el archivo mediante ruta relativa: '{ruta_relativa}'")
    
    try:
        # Pandas recibe la ruta relativa y busca desde el directorio de ejecución
        df = pd.read_csv(ruta_relativa)
        print(f"{LOG_DEBUG}Archivo leído correctamente usando rutas relativas.")
        return df

    except FileNotFoundError as e:
        print(f"\n{LOG_ERROR}No se encontró el archivo en la ruta relativa: '{ruta_relativa}'")
        raise e  # Re-lanzamos para que la suite de pruebas capture la falla real

    except pd.errors.EmptyDataError as e:
        print(f"\n{LOG_ERROR}El archivo existe pero está completamente vacío (0 bytes): '{ruta_relativa}'")
        raise e

    except pd.errors.ParserError as e:
        print(f"\n{LOG_ERROR}Error de parseo: El archivo CSV está corrupto o mal formateado.")
        raise e

    except PermissionError as e:
        print(f"\n{LOG_ERROR}Error de permisos: No hay acceso de lectura para el archivo.")
        raise e

    except Exception as e:
        print(f"\n{LOG_ERROR}Ocurrió un error inesperado al leer el archivo: {e}")
        raise e
