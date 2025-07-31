from typing import List, Dict, Any
import math

def calcular_porcentajes(especies_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calcular porcentajes para una lista de especies con cantidades de granos
    
    Args:
        especies_data: Lista de diccionarios con 'especie_id', 'cantidad_granos', etc.
    
    Returns:
        Lista actualizada con porcentajes calculados
    """
    total_granos = sum(especie.get('cantidad_granos', 0) for especie in especies_data)
    
    if total_granos == 0:
        return especies_data
    
    for especie in especies_data:
        cantidad = especie.get('cantidad_granos', 0)
        porcentaje = (cantidad / total_granos) * 100
        especie['porcentaje'] = round(porcentaje, 2)
        especie['total_granos'] = total_granos
    
    return especies_data

def calcular_estadisticas_analisis(analisis_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcular estadísticas de un análisis palinológico
    
    Args:
        analisis_data: Lista de análisis con porcentajes y cantidades
    
    Returns:
        Diccionario con estadísticas calculadas
    """
    if not analisis_data:
        return {}
    
    total_granos = sum(analisis.get('cantidad_granos', 0) for analisis in analisis_data)
    total_especies = len(analisis_data)
    porcentajes = [analisis.get('porcentaje', 0) for analisis in analisis_data]
    
    # Especie dominante (mayor porcentaje)
    especie_dominante = max(analisis_data, key=lambda x: x.get('porcentaje', 0))
    
    # Especies con porcentaje > 10%
    especies_importantes = [a for a in analisis_data if a.get('porcentaje', 0) > 10]
    
    # Diversidad (índice de Shannon)
    diversidad = 0
    if total_granos > 0:
        for analisis in analisis_data:
            p = analisis.get('cantidad_granos', 0) / total_granos
            if p > 0:
                diversidad -= p * math.log2(p)
    
    return {
        'total_granos': total_granos,
        'total_especies': total_especies,
        'especie_dominante': especie_dominante,
        'especies_importantes': especies_importantes,
        'diversidad_shannon': round(diversidad, 3),
        'porcentaje_total': sum(porcentajes),
        'promedio_porcentaje': round(sum(porcentajes) / total_especies, 2) if total_especies > 0 else 0
    }

def validar_analisis(especies_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validar datos de análisis palinológico
    
    Args:
        especies_data: Lista de especies con cantidades
    
    Returns:
        Diccionario con resultado de validación
    """
    total_granos = sum(especie.get('cantidad_granos', 0) for especie in especies_data)
    
    errores = []
    advertencias = []
    
    # Validar total mínimo de granos
    if total_granos < 100:
        errores.append("El total de granos debe ser al menos 100")
    
    # Validar que haya al menos una especie
    if len(especies_data) == 0:
        errores.append("Debe seleccionar al menos una especie")
    
    # Validar cantidades individuales
    for i, especie in enumerate(especies_data):
        cantidad = especie.get('cantidad_granos', 0)
        if cantidad < 0:
            errores.append(f"La cantidad de granos para la especie {i+1} no puede ser negativa")
        elif cantidad > 10000:
            advertencias.append(f"La cantidad de granos para la especie {i+1} es muy alta ({cantidad})")
    
    # Validar porcentajes
    if total_granos > 0:
        porcentajes = calcular_porcentajes(especies_data)
        total_porcentaje = sum(esp.get('porcentaje', 0) for esp in porcentajes)
        
        if abs(total_porcentaje - 100) > 0.1:  # Tolerancia de 0.1%
            advertencias.append(f"Los porcentajes no suman 100% (suma: {total_porcentaje:.1f}%)")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'advertencias': advertencias,
        'total_granos': total_granos
    }

def formatear_porcentaje(valor: float, decimales: int = 2) -> str:
    """
    Formatear un valor como porcentaje
    
    Args:
        valor: Valor decimal a formatear
        decimales: Número de decimales
    
    Returns:
        String formateado como porcentaje
    """
    return f"{valor:.{decimales}f}%"

def formatear_cantidad(valor: int) -> str:
    """
    Formatear una cantidad con separadores de miles
    
    Args:
        valor: Valor numérico
    
    Returns:
        String formateado
    """
    return f"{valor:,}".replace(",", ".") 