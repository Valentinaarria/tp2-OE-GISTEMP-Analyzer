import os

def obtener_ruta_relativa(carpeta, nombre_archivo):
    """
    Construye una ruta puramente relativa combinando la carpeta y el archivo.
    No utiliza abspath ni busca la ruta absoluta del script.
    """
    return os.path.join(carpeta, nombre_archivo)
