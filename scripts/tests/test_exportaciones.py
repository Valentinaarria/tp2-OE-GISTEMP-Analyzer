"""
Suite de pruebas unitarias para validar la correcta exportacion de archivos CSV
y la generacion de graficos estadisticos PNG en el modulo analizador.
"""

import unittest
import os
import shutil
import pandas as pd

from ..procesamiento.analizador import (
    generar_csv,
    generar_grafico_barras,
    generar_grafico_lineal,
    generar_grafico_tendencia
)

# ==========================================
# CONSTANTES DE PRUEBA 
# ==========================================
CARPETA_EXPORT_TEST = 'resultados_test_export'

COL_X = 'Eje_X'
COL_Y_BASE = 'Eje_Y_Base'
COL_Y_TENDENCIA = 'Eje_Y_Tendencia'
COL_LABEL_X = 'Año'
COL_LABEL_Y = 'Valor'

CSV_PRUEBA = 'prueba_exportacion.csv'
PNG_BARRAS = 'prueba_barras.png'
PNG_LINEAS = 'prueba_lineas.png'
PNG_TENDENCIA = 'prueba_tendencia.png'

TITULO_BARRAS = 'Test Barras'
TITULO_LINEAS = 'Test Lineas'
TITULO_TENDENCIA = 'Test Tendencia'

COLOR_AZUL = 'blue'
COLOR_ROJO = 'red'
BORDE_NEGRO = 'black'


class TestExportaciones(unittest.TestCase):
    """Clase que agrupa las pruebas de persistencia de datos y creacion de archivos PNG."""

    def setUp(self):
        """
        Preparamos un DataFrame generico en memoria y la carpeta temporal de salida.
        """
        self.carpeta_resultados_test = CARPETA_EXPORT_TEST
        os.makedirs(self.carpeta_resultados_test, exist_ok=True)

        self.df_mock = pd.DataFrame({
            COL_X: [2000, 2001, 2002],
            COL_Y_BASE: [1.5, 2.5, 3.5],
            COL_Y_TENDENCIA: [1.0, 2.0, 3.0]
        })

    def tearDown(self):
        """
        Limpiamos todos los archivos y estructuras generadas tras cada prueba de forma segura.
        """
        if os.path.exists(self.carpeta_resultados_test):
            shutil.rmtree(self.carpeta_resultados_test)

    def test_generar_csv(self):
        """
        Verifica que el archivo CSV se guarde en disco correctamente y preserve la integridad de los datos.
        """
        print("\n\n [TEST]: test_generar_csv")
        nombre_archivo = CSV_PRUEBA
        generar_csv(self.df_mock, nombre_archivo, self.carpeta_resultados_test)

        ruta_esperada = os.path.join(self.carpeta_resultados_test, nombre_archivo)
        existe_archivo = os.path.exists(ruta_esperada)

        df_leido = pd.read_csv(ruta_esperada) if existe_archivo else pd.DataFrame()
        longitud_obtenida = len(df_leido)
        valor_obtenido = df_leido.iloc[1][COL_Y_BASE] if longitud_obtenida > 0 else None

        print(f"Esperado: Archivo existe = True | Filas = 3 | Valor indice [1] = 2.5")
        print(f"Obtenido: Archivo existe = {existe_archivo} | Filas = {longitud_obtenida} | Valor indice [1] = {valor_obtenido}")

        self.assertTrue(existe_archivo)
        self.assertEqual(longitud_obtenida, 3)
        self.assertEqual(valor_obtenido, 2.5)

    def test_generar_grafico_barras(self):
        """
        Verifica que se procesen los datos y se genere fisicamente el archivo PNG del grafico de barras.
        """
        print("\n\n[TEST]: test_generar_grafico_barras")
        nombre_archivo = PNG_BARRAS

        generar_grafico_barras(
            df=self.df_mock,
            titulo=TITULO_BARRAS,
            nombre_archivo=nombre_archivo,
            carpeta_destino=self.carpeta_resultados_test,
            xValue=COL_X,
            yValue=COL_Y_BASE,
            xLabel=COL_LABEL_X,
            yLabel=COL_LABEL_Y,
            color=COLOR_AZUL,
            edge=BORDE_NEGRO
        )

        ruta_esperada = os.path.join(self.carpeta_resultados_test, nombre_archivo)
        existe_archivo = os.path.exists(ruta_esperada)

        print(f"Esperado: Archivo '{nombre_archivo}' creado = True")
        print(f"Obtenido: Archivo creado = {existe_archivo}")

        self.assertTrue(existe_archivo)

    def test_generar_grafico_lineal(self):
        """
        Verifica que se cree de forma correcta el archivo fisico PNG correspondiente al grafico lineal.
        """
        print("\n\n[TEST]: test_generar_grafico_lineal")
        nombre_archivo = PNG_LINEAS

        generar_grafico_lineal(
            df=self.df_mock,
            titulo=TITULO_LINEAS,
            nombre_archivo=nombre_archivo,
            carpeta_destino=self.carpeta_resultados_test,
            xValue=COL_X,
            yValue=COL_Y_BASE,
            color=COLOR_ROJO
        )

        ruta_esperada = os.path.join(self.carpeta_resultados_test, nombre_archivo)
        existe_archivo = os.path.exists(ruta_esperada)

        print(f"Esperado: Archivo '{nombre_archivo}' creado = True")
        print(f"Obtenido: Archivo creado = {existe_archivo}")

        self.assertTrue(existe_archivo)

    def test_generar_grafico_tendencia(self):
        """
        Verifica que se genere el archivo PNG comparativo cruzando los datos anuales con la media movil.
        """
        print("\n\n[TEST]: test_generar_grafico_tendencia")
        nombre_archivo = PNG_TENDENCIA

        generar_grafico_tendencia(
            df=self.df_mock,
            titulo=TITULO_TENDENCIA,
            nombre_archivo=nombre_archivo,
            carpeta_destino=self.carpeta_resultados_test,
            xValue=COL_X,
            yValue_base=COL_Y_BASE,
            yValue_tendencia=COL_Y_TENDENCIA
        )

        ruta_esperada = os.path.join(self.carpeta_resultados_test, nombre_archivo)
        existe_archivo = os.path.exists(ruta_esperada)

        print(f"Esperado: Archivo '{nombre_archivo}' creado = True")
        print(f"Obtenido: Archivo creado = {existe_archivo}")

        self.assertTrue(existe_archivo)


if __name__ == '__main__':
    unittest.main()
