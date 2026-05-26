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
    Maneja excepciones en caso de que el archivo no sea encontrado o esté corrupto.
    """
    # Generamos la ruta relativa pura
    ruta_relativa = obtener_ruta_relativa(carpeta_origen, nombre_archivo)

    print(f"{LOG_DEBUG}Intentando abrir el archivo mediante ruta relativa: '{ruta_relativa}'")
import pandas as pd

def cargar_csv(ruta_relativa):
    try:
        # Pandas recibe la ruta relativa y busca desde el directorio de ejecución
        df = pd.read_csv(ruta_relativa)
        print(f"{LOG_DEBUG}Archivo leído correctamente usando rutas relativas.")
        return df

    except FileNotFoundError as e:
        print(f"\n{LOG_ERROR}No se encontró el archivo en la ruta: '{ruta_relativa}'")
        raise e  

    except pd.errors.EmptyDataError as e:
        print(f"\n{LOG_ERROR}El archivo existe pero está completamente vacío: '{ruta_relativa}'")
        raise e  

    except pd.errors.ParserError as e:
        print(f"\n{LOG_ERROR}Error de parseo: El CSV está corrupto o mal formateado.")
        raise e

    except PermissionError as e:
        print(f"\n{LOG_ERROR}Error de permisos: No tenés acceso de lectura al archivo.")
        raise e

    except Exception as e:
        print(f"\n{LOG_ERROR}Ocurrió un error inesperado al leer el archivo: {e}")
        raise e
