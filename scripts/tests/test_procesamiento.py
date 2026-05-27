"""
Suite de pruebas unitarias para validar las funciones de procesamiento
y analisis de datos climaticos del modulo analizador.
"""

import unittest
import pandas as pd

from ..procesamiento.analizador import (
    procesar_top5,
    procesar_decadas,
    procesar_tendencia,
    procesar_estacionalidad_mensual
)

# ==========================================
# CONSTANTES DE PRUEBA 
# ==========================================
COL_YEAR = 'Year'
COL_MEAN = 'Mean'
COL_SOURCE = 'Source'
COL_DECADE = 'Decade'
COL_ROLLING = 'Rolling_Mean'
COL_MES = 'Mes'

AGENCIA_GISTEMP = 'GISTEMP'


class TestProcesamientoDatos(unittest.TestCase):
    """Clase que agrupa las pruebas de logica de negocio y calculos estadisticos."""

    def setUp(self):
        """
        Preparamos los DataFrames falsos en memoria para las pruebas.
        """
        self.df_anual_mock = pd.DataFrame({
            COL_YEAR: [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000],
            COL_MEAN: [1.0,  2.0,  3.0,  4.0,  5.0,  6.0,  7.0,  8.0,  9.0,  10.0, 11.0],
            COL_SOURCE: [AGENCIA_GISTEMP] * 11
        })

        self.df_mensual_mock = pd.DataFrame({
            COL_YEAR: ['2020-01', '2020-02', '2021-01', '2021-02'],
            COL_MEAN: [0.5,       1.5,       1.5,       2.5],
            COL_SOURCE: [AGENCIA_GISTEMP] * 4
        })

    def test_procesar_top5(self):
        """
        Verifica que retorne un DF de 5 filas, ordenado de mayor a menor anomalio.
        """
        print("\n\n[TEST]: test_procesar_top5")
        df_resultado = procesar_top5(self.df_anual_mock)

        # Valores reales obtenidos para inspeccion visual
        longitud_obtenida = len(df_resultado)
        primer_anio_obtenido = df_resultado.iloc[0][COL_YEAR]
        quinto_anio_obtenido = df_resultado.iloc[4][COL_YEAR]

        print(f"Esperado: Longitud = 5 | Primero = 2000 | Quinto = 1996")
        print(f"Obtenido: Longitud = {longitud_obtenida} | Primero = {primer_anio_obtenido} | Quinto = {quinto_anio_obtenido}")

        self.assertEqual(longitud_obtenida, 5)
        self.assertEqual(primer_anio_obtenido, 2000)
        self.assertEqual(quinto_anio_obtenido, 1996)

    def test_procesar_decadas(self):
        """
        Verifica que agrupe por decadas correctamente y calcule el promedio.
        """
        print("\n\n[TEST]: test_procesar_decadas")
        df_resultado = procesar_decadas(self.df_anual_mock)

        longitud_obtenida = len(df_resultado)
        fila_90 = df_resultado[df_resultado[COL_DECADE] == 1990]
        promedio_90_obtenido = fila_90.iloc[0][COL_MEAN]

        print(f"Esperado: Cantidad decadas = 2 | Promedio decada 1990 = 5.5")
        print(f"Obtenido: Cantidad decadas = {longitud_obtenida} | Promedio decada 1990 = {promedio_90_obtenido}")

        self.assertEqual(longitud_obtenida, 2)
        self.assertAlmostEqual(promedio_90_obtenido, 5.5)

    def test_procesar_tendencia(self):
        """
        Verifica que se agregue y calcule correctamente la columna de media movil.
        """
        print("\n\n[TEST]: test_procesar_tendencia")
        df_resultado = procesar_tendencia(self.df_anual_mock)

        tiene_columna = COL_ROLLING in df_resultado.columns
        valor_tendencia_obtenido = df_resultado.loc[df_resultado[COL_YEAR] == 1999, COL_ROLLING].values[0]

        print(f"Esperado: Columna '{COL_ROLLING}' presente | Media movil 1999 = 5.5")
        print(f"Obtenido: Columna presente = {tiene_columna} | Media movil 1999 = {valor_tendencia_obtenido}")

        self.assertIn(COL_ROLLING, df_resultado.columns)
        self.assertAlmostEqual(valor_tendencia_obtenido, 5.5)

    def test_procesar_estacionalidad_mensual(self):
        """
        Verifica que se agrupe la informacion por mes de forma correcta.
        """
        print("\n\n[TEST]: test_procesar_estacionalidad_mensual")
        df_resultado = procesar_estacionalidad_mensual(self.df_mensual_mock)

        longitud_obtenida = len(df_resultado)
        fila_enero = df_resultado[df_resultado[COL_MES] == '01']
        promedio_enero_obtenido = fila_enero.iloc[0][COL_MEAN]

        print(f"Esperado: Cantidad meses = 2 | Promedio Enero ('01') = 1.0")
        print(f"Obtenido: Cantidad meses = {longitud_obtenida} | Promedio Enero ('01') = {promedio_enero_obtenido}")

        self.assertEqual(longitud_obtenida, 2)
        self.assertAlmostEqual(promedio_enero_obtenido, 1.0)


if __name__ == '__main__':
    unittest.main()
