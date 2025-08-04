from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

def formatear_fecha(fecha, formato_entrada: str = "%Y-%m-%d", formato_salida: str = "%d/%m/%Y") -> str:
    """
    Formatear fecha de un formato a otro
    
    Args:
        fecha: Fecha como string, datetime.date, o datetime.datetime
        formato_entrada: Formato de entrada (solo para strings)
        formato_salida: Formato de salida
    
    Returns:
        Fecha formateada
    """
    try:
        # Si es un objeto datetime.date o datetime.datetime
        if hasattr(fecha, 'strftime'):
            return fecha.strftime(formato_salida)
        
        # Si es un string
        if isinstance(fecha, str):
            fecha_obj = datetime.strptime(fecha, formato_entrada)
            return fecha_obj.strftime(formato_salida)
        
        # Si es None o vacío
        if not fecha:
            return ""
        
        # Para cualquier otro tipo, intentar convertirlo a string
        return str(fecha)
    except:
        return str(fecha) if fecha else ""

def formatear_fecha_simple(fecha) -> str:
    """
    Formatear fecha de manera simple para componentes de Streamlit
    
    Args:
        fecha: Fecha como string, datetime.date, o datetime.datetime
    
    Returns:
        Fecha como string en formato YYYY-MM-DD
    """
    try:
        # Si es un objeto datetime.date o datetime.datetime
        if hasattr(fecha, 'strftime'):
            return fecha.strftime("%Y-%m-%d")
        
        # Si es un string, retornarlo tal como está
        if isinstance(fecha, str):
            return fecha
        
        # Si es None o vacío
        if not fecha:
            return ""
        
        # Para cualquier otro tipo, intentar convertirlo a string
        return str(fecha)
    except:
        return str(fecha) if fecha else ""

def formatear_nombre_completo(nombre: str, apellido: str) -> str:
    """
    Formatear nombre completo
    
    Args:
        nombre: Nombre
        apellido: Apellido
    
    Returns:
        Nombre completo formateado
    """
    return f"{nombre} {apellido}".strip()

def formatear_especie(nombre_comun: str, nombre_cientifico: str) -> str:
    """
    Formatear nombre de especie
    
    Args:
        nombre_comun: Nombre común
        nombre_cientifico: Nombre científico
    
    Returns:
        Especie formateada
    """
    if nombre_comun:
        return f"{nombre_comun} ({nombre_cientifico})"
    else:
        return nombre_cientifico

def crear_dataframe_analisis(analisis_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Crear DataFrame para mostrar análisis palinológico
    
    Args:
        analisis_data: Lista de análisis
    
    Returns:
        DataFrame formateado
    """
    if not analisis_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(analisis_data)
    
    # Formatear columnas
    if 'nombre_comun' in df.columns and 'nombre_cientifico' in df.columns:
        df['Especie'] = df.apply(lambda x: formatear_especie(x['nombre_comun'], x['nombre_cientifico']), axis=1)
    
    if 'cantidad_granos' in df.columns:
        df['Granos'] = df['cantidad_granos'].apply(lambda x: f"{x:,}".replace(",", "."))
    
    if 'porcentaje' in df.columns:
        df['Porcentaje'] = df['porcentaje'].apply(lambda x: f"{x:.2f}%")
    
    # Seleccionar columnas para mostrar
    columnas_mostrar = []
    if 'Especie' in df.columns:
        columnas_mostrar.append('Especie')
    if 'Granos' in df.columns:
        columnas_mostrar.append('Granos')
    if 'Porcentaje' in df.columns:
        columnas_mostrar.append('Porcentaje')
    if 'marca_especial' in df.columns:
        columnas_mostrar.append('marca_especial')
    
    return df[columnas_mostrar] if columnas_mostrar else df

def crear_dataframe_tambores(tambores_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Crear DataFrame para mostrar tambores
    
    Args:
        tambores_data: Lista de tambores
    
    Returns:
        DataFrame formateado
    """
    if not tambores_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(tambores_data)
    
    # Formatear columnas
    if 'apicultor_nombre' in df.columns and 'apicultor_apellido' in df.columns:
        df['Apicultor'] = df.apply(lambda x: formatear_nombre_completo(x['apicultor_nombre'], x['apicultor_apellido']), axis=1)
    
    if 'fecha_extraccion' in df.columns:
        df['Fecha Extracción'] = df['fecha_extraccion'].apply(lambda x: formatear_fecha(x) if x else 'N/A')
    
    # Seleccionar columnas para mostrar
    columnas_mostrar = []
    if 'num_registro' in df.columns:
        columnas_mostrar.append('num_registro')
    if 'Apicultor' in df.columns:
        columnas_mostrar.append('Apicultor')
    if 'Fecha Extracción' in df.columns:
        columnas_mostrar.append('Fecha Extracción')
    
    return df[columnas_mostrar] if columnas_mostrar else df

def formatear_resumen_analisis(analisis_completo: Dict[str, Any]) -> str:
    """
    Crear resumen formateado de un análisis
    
    Args:
        analisis_completo: Datos completos del análisis
    
    Returns:
        Resumen formateado
    """
    if not analisis_completo:
        return "No hay datos de análisis"
    
    pool_info = analisis_completo.get('pool_info', {})
    analisis_especies = analisis_completo.get('analisis_especies', [])
    tambores = analisis_completo.get('tambores', [])
    
    resumen = f"""
**Análisis Palinológico - Pool #{pool_info.get('id_pool', 'N/A')}**

**Información del Pool:**
- **Analista:** {formatear_nombre_completo(pool_info.get('analista_nombres', ''), pool_info.get('analista_apellidos', ''))}
- **Fecha de Análisis:** {formatear_fecha(pool_info.get('fecha_analisis', ''))}
- **Total de Especies:** {len(analisis_especies)}
- **Total de Granos:** {sum(esp.get('cantidad_granos', 0) for esp in analisis_especies):,}
- **Tambores Analizados:** {len(tambores)}

**Especies Identificadas:**
"""
    
    for i, especie in enumerate(analisis_especies[:5], 1):  # Mostrar solo las 5 primeras
        resumen += f"{i}. {especie.get('nombre_comun', 'N/A')} - {especie.get('cantidad_granos', 0)} granos\n"
    
    if len(analisis_especies) > 5:
        resumen += f"... y {len(analisis_especies) - 5} especies más\n"
    
    return resumen

def formatear_estadisticas(estadisticas: Dict[str, Any]) -> str:
    """
    Formatear estadísticas para mostrar
    
    Args:
        estadisticas: Diccionario con estadísticas
    
    Returns:
        Estadísticas formateadas
    """
    if not estadisticas:
        return "No hay estadísticas disponibles"
    
    texto = f"""
**Estadísticas del Análisis:**

- **Total de Granos:** {estadisticas.get('total_granos', 0):,}
- **Total de Especies:** {estadisticas.get('total_especies', 0)}
- **Diversidad (Shannon):** {estadisticas.get('diversidad_shannon', 0):.3f}
- **Porcentaje Total:** {estadisticas.get('porcentaje_total', 0):.2f}%
- **Promedio por Especie:** {estadisticas.get('promedio_porcentaje', 0):.2f}%

**Especie Dominante:**
{estadisticas.get('especie_dominante', {}).get('nombre_comun', 'N/A')} - {estadisticas.get('especie_dominante', {}).get('cantidad_granos', 0)} granos

**Especies Importantes (>10%):**
"""
    
    especies_importantes = estadisticas.get('especies_importantes', [])
    for especie in especies_importantes:
        texto += f"- {especie.get('nombre_comun', 'N/A')}: {especie.get('cantidad_granos', 0)} granos\n"
    
    return texto 