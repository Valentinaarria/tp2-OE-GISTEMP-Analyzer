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
        """Preparamos los DataFrames falsos en memoria para las pruebas."""
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
        """Verifica que retorne un DF de 5 filas, ordenado de mayor a menor anomalio."""
        df_resultado = procesar_top5(self.df_anual_mock)

        self.assertEqual(len(df_resultado), 5, msg="La longitud del DataFrame Top 5 deberia ser de exactamente 5 filas.")
        self.assertEqual(df_resultado.iloc[0][COL_YEAR], 2000, msg="El primer elemento del Top 5 deberia ser el anio 2000.")
        self.assertEqual(df_resultado.iloc[4][COL_YEAR], 1996, msg="El quinto elemento del Top 5 deberia ser el anio 1996.")

    def test_procesar_decadas(self):
        """Verifica que agrupe por decadas correctamente y calcule el promedio."""
        df_resultado = procesar_decadas(self.df_anual_mock)

        self.assertEqual(len(df_resultado), 2, msg="Se esperaban exactamente 2 decadas procesadas (1990 y 2000).")
        
        fila_90 = df_resultado[df_resultado[COL_DECADE] == 1990]
        self.assertAlmostEqual(fila_90.iloc[0][COL_MEAN], 5.5, msg="El promedio de anomalia calculado para la decada de 1990 deberia ser 5.5.")

    def test_procesar_tendencia(self):
        """Verifica que se agregue y calcule correctamente la columna de media movil."""
        df_resultado = procesar_tendencia(self.df_anual_mock)

        self.assertIn(COL_ROLLING, df_resultado.columns, msg=f"La columna calculada '{COL_ROLLING}' no se encuentra en el DataFrame resultante.")
        
        valor_tendencia_obtenido = df_resultado.loc[df_resultado[COL_YEAR] == 1999, COL_ROLLING].values[0]
        self.assertAlmostEqual(valor_tendencia_obtenido, 5.5, msg="La media movil acumulada para el anio 1999 deberia ser exactamente 5.5.")

    def test_procesar_estacionalidad_mensual(self):
        """Verifica que se agrupe la informacion por mes de forma correcta."""
        df_resultado = procesar_estacionalidad_mensual(self.df_mensual_mock)

        self.assertEqual(len(df_resultado), 2, msg="Se esperaban exactamente 2 meses agrupados en el resultado estacional.")
        
        fila_enero = df_resultado[df_resultado[COL_MES] == '01']
        self.assertAlmostEqual(fila_enero.iloc[0][COL_MEAN], 1.0, msg="El promedio estacional calculado para el mes de Enero ('01') deberia ser 1.0.")


if __name__ == '__main__':
    unittest.main()
