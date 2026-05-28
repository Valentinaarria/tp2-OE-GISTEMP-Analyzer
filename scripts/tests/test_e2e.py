import unittest
import os
import io

# Importamos la función orquestadora principal
from ..procesamiento.analizador import main

class TestPipelineEndToEnd(unittest.TestCase):
    """
    Suite de pruebas de integración End-to-End (E2E) para el analizador climático.
    
    Verifica que el flujo de ejecución completo (extracción, transformación,
    cálculo de métricas y renderizado de gráficos) funcione correctamente de principio
    a fin, asegurando la integridad física y el contenido mínimo de las exportaciones.
    """

    # --- CONSTANTES DE CONFIGURACIÓN DEL TEST ---
    CARPETA_RESULTADOS = 'resultados'
    ARCHIVOS_ESPERADOS = [
        '01_top5_anuales.csv',
        '01_grafico_top5.png',
        '02_decadas.csv',
        '02_grafico_decadas.png',
        '03_tendencia_historica.csv',
        '03_grafico_tendencia.png',
        '05_promedio_por_mes.csv',
        '05_grafico_estacionalidad.png'
    ]

    def test_pipeline_completo(self):
        """
        Ejecuta el pipeline principal y valida la persistencia y robustez de los reportes.
        
        Prueba que la función main() no lance excepciones imprevistas, que genere
        correctamente la carpeta contenedora y que cada archivo del inventario
        exista en disco con un tamaño superior a 0 bytes.
        """
        # 1. Interceptamos la salida estándar (consola) para evitar logs ruidosos durante el test
        salida_capturada = io.StringIO()
        import sys  # Import local temporal solo para la redirección de flujos de consola
        sys.stdout = salida_capturada

        try:
            # 2. Ejecución integral del flujo de negocio
            main()
        except Exception as e:
            self.fail(f"El pipeline principal falló abruptamente durante la ejecución. Error: {e}")
        finally:
            # 3. Restauramos la consola al estado original del sistema operativo
            sys.stdout = sys.__stdout__

        # 4. Validamos la existencia física del directorio de salida mediante manejo defensivo
        try:
            existe_carpeta = os.path.exists(self.CARPETA_RESULTADOS)
            self.assertTrue(existe_carpeta, f"Error: La carpeta '{self.CARPETA_RESULTADOS}' no fue creada en la raíz.")
        except Exception as e:
            self.fail(f"Ocurrió un error inesperado al intentar acceder al directorio de resultados: {e}")

        # 5. Iteración del inventario de constantes mediante capturas try-except controladas
        for archivo in self.ARCHIVOS_ESPERADOS:
            ruta_completa = os.path.join(self.CARPETA_RESULTADOS, archivo)

            # Control de flujo y aserciones para la existencia y metadatos del archivo
            try:
                # Verificación de presencia en el sistema de archivos
                existe_archivo = os.path.exists(ruta_completa)
                self.assertTrue(existe_archivo, f"Fallo Crítico: El artefacto esperado '{archivo}' no se encuentra en disco.")

                # Verificación de peso para asegurar que no se hayan guardado archivos corruptos de 0 bytes
                tamano_archivo = os.path.getsize(ruta_completa)
                self.assertGreater(tamano_archivo, 0, f"Fallo Crítico: El archivo '{archivo}' se creó pero está vacío (0 bytes).")
                
            except FileNotFoundError:
                self.fail(f"Fallo de Entrada/Salida: No se pudo localizar el archivo físico en la ruta: {ruta_completa}")
            except OSError as os_err:
                self.fail(f"Error del Sistema Operativo al leer los metadatos de '{archivo}': {os_err}")
            except Exception as unexp_err:
                self.fail(f"Error imprevisto durante la validación del archivo '{archivo}': {unexp_err}")

if __name__ == '__main__':
    unittest.main()
