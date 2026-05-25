
# funciones_aqualimpia.py
# Archivo externo con funciones reutilizables para el proyecto AquaLimpia S.A.

import pandas as pd
import numpy as np

def cargar_datos(ruta_archivo):
    """
    Carga un dataset desde un archivo Excel.
    """
    df = pd.read_excel(ruta_archivo)
    print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df

def calcular_eficiencia_dbo(df, col_entrada='DBO_entrada_mg_L', col_salida='DBO_salida_mg_L'):
    """
    Calcula la eficiencia de remocion de DBO.
    """
    eficiencia = ((df[col_entrada] - df[col_salida]) / df[col_entrada]) * 100
    return eficiencia.round(1)

def generar_alertas_eficiencia(eficiencia):
    """
    Genera alertas segun el nivel de eficiencia.
    """
    alertas = np.where(eficiencia >= 85, 'Optimo',
               np.where(eficiencia >= 70, 'Atencion', 'Critico'))
    return pd.Series(alertas)

def resumen_por_planta(df, columna_analisis, columna_agrupacion='planta'):
    """
    Genera un resumen estadistico agrupado por planta.
    """
    resumen = df.groupby(columna_agrupacion)[columna_analisis].agg(['mean', 'std']).round(2)
    resumen.columns = ['Media', 'Desviacion Estandar']
    return resumen

def exportar_reporte(df, columnas, nombre_archivo):
    """
    Exporta un reporte a Excel con las columnas seleccionadas.
    """
    try:
        df[columnas].to_excel(nombre_archivo, index=False)
        print(f"Reporte exportado: {nombre_archivo}")
        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False
