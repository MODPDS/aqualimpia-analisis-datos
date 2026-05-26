# funciones_aqualimpia.py
# Archivo externo con funciones reutilizables para el proyecto AquaLimpia S.A.
# Incorpora NumPy, SciPy y Joblib cumpliendo las buenas prácticas de programación.

import pandas as pd
import numpy as np
from scipy import stats  # <--- NUEVO: Para análisis estadístico avanzado
import joblib            # <--- NUEVO: Para persistencia eficiente de objetos y datos
import os

def cargar_datos(ruta_archivo):
    """
    Carga un dataset desde un archivo Excel.
    """
    df = pd.read_excel(ruta_archivo)
    print(f"Datos cargados exitosamente: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df

def calcular_eficiencia_dbo(df, col_entrada='DBO_entrada_mg_L', col_salida='DBO_salida_mg_L'):
    """
    Calcula la eficiencia de remoción de DBO porcentual usando NumPy.
    """
    # Evita división por cero en caso de datos corruptos de entrada
    entrada = np.where(df[col_entrada] == 0, np.nan, df[col_entrada])
    eficiencia = ((entrada - df[col_salida]) / entrada) * 100
    return eficiencia.round(1)

def generar_alertas_eficiencia(eficiencia):
    """
    Genera alertas categóricas según el nivel de eficiencia utilizando condiciones vectorizadas de NumPy.
    """
    alertas = np.where(eficiencia >= 85, 'Optimo',
               np.where(eficiencia >= 70, 'Atencion', 'Critico'))
    return pd.Series(alertas)

def resumen_por_planta(df, columna_analisis, columna_agrupacion='planta'):
    """
    Genera un resumen estadístico básico agrupado por planta.
    """
    resumen = df.groupby(columna_agrupacion)[columna_analisis].agg(['mean', 'std']).round(2)
    resumen.columns = ['Media', 'Desviacion Estandar']
    return resumen

def realizar_test_hipotesis_scipy(df, col_eficiencia='eficiencia_DBO', col_planta='planta'):
    """
    NUEVO: Utiliza SciPy Stats para evaluar si existen diferencias significativas
    en la eficiencia de remoción entre las diferentes plantas de tratamiento.
    Responde científicamente a la Pregunta de Investigación N°1.
    """
    print("\n--- EJECUTANDO ANÁLISIS ESTADÍSTICO CON SCIPY ---")
    plantas = df[col_planta].unique()
    grupos = [df[df[col_planta] == p][col_eficiencia].dropna() for p in plantas]
    
    # Realizar la prueba no paramétrica de Kruskal-Wallis (ideal para datos operativos reales)
    stat, p_valor = stats.kruskal(*grupos)
    
    print(f"Resultado del Test (Kruskal-Wallis): Estadístico = {stat:.4f}, p-valor = {p_valor:.4e}")
    if p_valor < 0.05:
        print("Conclusión: El p-valor es menor a 0.05. Existen diferencias ESTADÍSTICAMENTE SIGNIFICATIVAS en la eficiencia entre las plantas.")
    else:
        print("Conclusión: El p-valor es mayor o igual a 0.05. NO existen diferencias significativas en la eficiencia entre las plantas.")
        
    return stat, p_valor

def guardar_datos_procesados_joblib(df, nombre_archivo='aqualimpia_procesado.pkl'):
    """
    NUEVO: Utiliza Joblib para serializar y almacenar en caché el DataFrame final procesado,
    garantizando la reproducibilidad y rapidez en la carga de datos del flujo de trabajo.
    """
    print(f"\n--- ALMACENANDO RESPALDO DE DATOS CON JOBLIB ---")
    joblib.dump(df, nombre_archivo)
    print(f"Dataframe guardado eficientemente en: {os.path.abspath(nombre_archivo)}")
    return nombre_archivo

def exportar_reportes_excel(df, columna_agrupacion='planta'):
    """
    Exporta archivos Excel independientes para cada planta (Reportes diferenciados).
    """
    plantas = df[columna_agrupacion].unique()
    for planta in plantas:
        df_planta = df[df[columna_agrupacion] == planta]
        nombre_archivo = f"Reporte_{planta.replace(' ', '_')}.xlsx"
        df_planta.to_excel(nombre_archivo, index=False)
        print(f"Reporte exportado exitosamente: {nombre_archivo}")
