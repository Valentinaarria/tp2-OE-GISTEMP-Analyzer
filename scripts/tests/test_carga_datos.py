"""
Suite de pruebas unitarias para validar las funciones de carga de datos
y el rutado relativo del proyecto.
"""

import unittest
import os
import pandas as pd

from ..procesamiento.rutas import obtener_ruta_relativa
from ..procesamiento.carga_de_datos import cargar_csv

# ==========================================
# CONSTANTES DE PRUEBA (Buenas Prácticas)
# ==========================================
CARPETA_TEST = 'datos_test'
ARCHIVO_TEST = 'dummy.csv'
ARCHIVO_FANTASMA = 'archivo_fantasma.csv'
CONTENIDO_DUMMY = "Year,Mean,Source\n2020,0.98,GISTEMP\n"

CARPETA_ESPERADA_RUTA = "datos"
ARCHIVO_ESPERADO_RUTA = "test.csv"

COLUMNA_ANIO = 'Year'
VALOR_ANIO_ESPERADO = 2020


class TestCargaYRutado(unittest.TestCase):
    """Clase que agrupa las pruebas de carga de archivos CSV y gestión de rutas."""

    def setUp(self):
        """
        Configura el entorno de prueba creando un directorio y un archivo CSV temporal.
        """
        self.carpeta_test = CARPETA_TEST
        self.archivo_test = ARCHIVO_TEST
        os.makedirs(self.carpeta_test, exist_ok=True)

        self.ruta_completa = os.path.join(self.carpeta_test, self.archivo_test)

        with open(self.ruta_completa, 'w', encoding='utf-8') as f:
            f.write(CONTENIDO_DUMMY)

    def tearDown(self):
        """
        Limpia el entorno eliminando el archivo y directorio creados en el setUp.
        """
        if os.path.exists(self.ruta_completa):
            os.remove(self.ruta_completa)
        if os.path.exists(self.carpeta_test):
            os.rmdir(self.carpeta_test)

    def test_obtener_ruta_relativa(self):
        """
        Verifica que la funcion construya correctamente rutas relativas segun el SO.
        """
        ruta_esperada = os.path.join(CARPETA_ESPERADA_RUTA, ARCHIVO_ESPERADO_RUTA)
        ruta_obtenida = obtener_ruta_relativa(CARPETA_ESPERADA_RUTA, ARCHIVO_ESPERADO_RUTA)
        self.assertEqual(ruta_obtenida, ruta_esperada)

    def test_cargar_csv_exito(self):
        """
        Valida que un archivo existente se cargue correctamente como un DataFrame de Pandas.
        """
        df = cargar_csv(self.archivo_test, carpeta_origen=self.carpeta_test)
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0][COLUMNA_ANIO], VALOR_ANIO_ESPERADO)

    def test_cargar_csv_fallo(self):
        """
        Asegura que intentar cargar un archivo inexistente lance una excepcion FileNotFoundError.
        """
        with self.assertRaises(FileNotFoundError):
            cargar_csv(ARCHIVO_FANTASMA, carpeta_origen=self.carpeta_test)


if __name__ == '__main__':
    unittest.main()
