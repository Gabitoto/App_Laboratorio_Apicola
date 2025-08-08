from models.base_model import BaseModel
from typing import List, Dict, Any, Optional
from utils.calculators import calcular_porcentajes

class AnalisisPalinologico(BaseModel):
    """Modelo para la tabla analisis_palinologico"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "analisis_palinologico"
    
    def get_all_analisis(self) -> List[Dict[str, Any]]:
        """Obtener todos los análisis ordenados por fecha"""
        return self.get_all(self.table_name, "id_palinologico DESC")
    
    def get_analisis_by_id(self, analisis_id: int) -> Optional[Dict[str, Any]]:
        """Obtener análisis por ID"""
        return self.get_by_id(self.table_name, "id_palinologico", analisis_id)
    
    def create_analisis(self, id_pool: int, id_especie: int, cantidad_granos: int, 
                       marca_especial: str = None) -> Optional[int]:
        """Crear un nuevo análisis palinológico"""
        data = {
            'id_pool': id_pool,
            'id_especie': id_especie,
            'cantidad_granos': cantidad_granos,
            'marca_especial': marca_especial
        }
        return self.insert(self.table_name, data)
    
    def update_analisis(self, analisis_id: int, **kwargs) -> bool:
        """Actualizar datos de un análisis"""
        return self.update(self.table_name, "id_palinologico", analisis_id, kwargs)
    
    def delete_analisis(self, analisis_id: int) -> bool:
        """Eliminar un análisis"""
        return self.delete(self.table_name, "id_palinologico", analisis_id)
    
    def get_analisis_by_pool(self, pool_id: int) -> List[Dict[str, Any]]:
        """Obtener todos los análisis de un pool específico con porcentajes calculados"""
        query = """
            SELECT ap.*, e.nombre_comun, e.nombre_cientifico, e.familia
            FROM analisis_palinologico ap
            INNER JOIN especies e ON ap.id_especie = e.id_especie
            WHERE ap.id_pool = %s
            ORDER BY ap.cantidad_granos DESC
        """
        analisis_data = self.execute_custom_query(query, (pool_id,)) or []
        
        # Calcular porcentajes si hay datos
        if analisis_data:
            total_granos = sum(analisis['cantidad_granos'] for analisis in analisis_data)
            for analisis in analisis_data:
                if total_granos > 0:
                    analisis['porcentaje'] = round((analisis['cantidad_granos'] / total_granos) * 100, 2)
                else:
                    analisis['porcentaje'] = 0.0
        
        return analisis_data
    
    def get_analisis_completo(self, pool_id: int) -> Dict[str, Any]:
        """Obtener análisis completo con detalles del pool y especies"""
        # Debug: Imprimir pool_id que se está consultando
        print(f"Consultando análisis completo para pool {pool_id}")
        
        # Obtener información del pool
        pool_query = """
            SELECT p.*, a.nombres as analista_nombres, a.apellidos as analista_apellidos
            FROM pool p
            INNER JOIN analista a ON p.id_analista = a.id_analista
            WHERE p.id_pool = %s
        """
        pool_info = self.execute_custom_query(pool_query, (pool_id,))
        
        # Debug: Verificar información del pool
        print(f"Información del pool: {pool_info}")
        
        if not pool_info:
            print(f"No se encontró información del pool {pool_id}")
            return None
        
        # Obtener análisis de especies
        analisis_especies = self.get_analisis_by_pool(pool_id)
        
        # Debug: Verificar análisis de especies
        print(f"Análisis de especies encontrados: {len(analisis_especies)}")
        print(f"Datos de análisis: {analisis_especies}")
        
        # Obtener tambores del pool
        tambores_query = """
            SELECT mt.*, a.nombre as apicultor_nombre, a.apellido as apicultor_apellido
            FROM muestra_tambor mt
            INNER JOIN compone_pool cp ON mt.id_tambor = cp.id_tambor
            INNER JOIN apicultor a ON mt.id_apicultor = a.id_apicultor
            WHERE cp.id_pool = %s
            ORDER BY mt.num_registro
        """
        tambores = self.execute_custom_query(tambores_query, (pool_id,)) or []
        
        # Debug: Verificar tambores
        print(f"Tambores encontrados: {len(tambores)}")
        
        resultado = {
            'pool_info': pool_info[0],
            'analisis_especies': analisis_especies,
            'tambores': tambores,
            'total_granos': sum(analisis['cantidad_granos'] for analisis in analisis_especies),
            'total_especies': len(analisis_especies)
        }
        
        # Debug: Verificar resultado final
        print(f"Resultado final: {resultado}")
        
        return resultado
    
    def get_analisis_by_date_range(self, fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """Obtener análisis en un rango de fechas"""
        query = """
            SELECT ap.*, e.nombre_comun, e.nombre_cientifico, p.fecha_analisis,
                   a.nombres as analista_nombres, a.apellidos as analista_apellidos,
                   p.id_analista, a.id_analista as analista_id
            FROM analisis_palinologico ap
            INNER JOIN especies e ON ap.id_especie = e.id_especie
            INNER JOIN pool p ON ap.id_pool = p.id_pool
            INNER JOIN analista a ON p.id_analista = a.id_analista
            WHERE p.fecha_analisis BETWEEN %s AND %s
            ORDER BY p.fecha_analisis DESC, ap.cantidad_granos DESC
        """
        return self.execute_custom_query(query, (fecha_inicio, fecha_fin)) or []
    
    def get_analisis_by_analista(self, analista_id: int) -> List[Dict[str, Any]]:
        """Obtener análisis de un analista específico"""
        query = """
            SELECT ap.*, e.nombre_comun, e.nombre_cientifico, p.fecha_analisis
            FROM analisis_palinologico ap
            INNER JOIN especies e ON ap.id_especie = e.id_especie
            INNER JOIN pool p ON ap.id_pool = p.id_pool
            WHERE p.id_analista = %s
            ORDER BY p.fecha_analisis DESC, ap.cantidad_granos DESC
        """
        return self.execute_custom_query(query, (analista_id,)) or []
    
    def get_estadisticas_especies(self) -> List[Dict[str, Any]]:
        """Obtener estadísticas de especies más frecuentes"""
        query = """
            SELECT e.nombre_comun, e.nombre_cientifico, e.familia,
                   COUNT(ap.id_palinologico) as total_analisis,
                   SUM(ap.cantidad_granos) as total_granos
            FROM especies e
            INNER JOIN analisis_palinologico ap ON e.id_especie = ap.id_especie
            GROUP BY e.id_especie, e.nombre_comun, e.nombre_cientifico, e.familia
            ORDER BY total_analisis DESC, total_granos DESC
        """
        return self.execute_custom_query(query) or []
    
    def save_analisis_completo(self, pool_id: int, especies_data: List[Dict[str, Any]]) -> bool:
        """Guardar análisis completo para un pool"""
        try:
            # Debug: Imprimir datos que se van a guardar
            print(f"Guardando análisis para pool {pool_id}")
            print(f"Datos a guardar: {especies_data}")
            
            # Preparar datos para inserción
            insert_data = []
            for especie in especies_data:
                insert_data.append((
                    pool_id,
                    especie['especie_id'],
                    especie['cantidad_granos'],
                    especie.get('marca_especial')
                ))
            
            # Debug: Imprimir datos preparados
            print(f"Datos preparados para inserción: {insert_data}")
            
            # Insertar todos los análisis
            query = """
                INSERT INTO analisis_palinologico 
                (id_pool, id_especie, cantidad_granos, marca_especial)
                VALUES (%s, %s, %s, %s)
            """
            result = self.execute_many(query, insert_data)
            
            # Debug: Verificar resultado
            print(f"Resultado de inserción: {result}")
            
            return result is not None and result > 0
            
        except Exception as e:
            print(f"Error al guardar análisis completo: {str(e)}")
            return False 