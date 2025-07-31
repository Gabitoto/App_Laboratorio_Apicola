from models.base_model import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Pool(BaseModel):
    """Modelo para la tabla pool"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "pool"
    
    def get_all_pools(self) -> List[Dict[str, Any]]:
        """Obtener todos los pools ordenados por fecha de análisis"""
        return self.get_all(self.table_name, "fecha_analisis DESC")
    
    def get_pool_by_id(self, pool_id: int) -> Optional[Dict[str, Any]]:
        """Obtener pool por ID"""
        return self.get_by_id(self.table_name, "id_pool", pool_id)
    
    def create_pool(self, id_analista: int, fecha_analisis: str, num_registro: str = None, observaciones: str = None) -> Optional[int]:
        """Crear un nuevo pool"""
        data = {
            'id_analista': id_analista,
            'fecha_analisis': fecha_analisis,
            'num_registro': num_registro,
            'observaciones': observaciones
        }
        return self.insert(self.table_name, data)
    
    def update_pool(self, pool_id: int, **kwargs) -> bool:
        """Actualizar datos de un pool"""
        return self.update(self.table_name, "id_pool", pool_id, kwargs)
    
    def delete_pool(self, pool_id: int) -> bool:
        """Eliminar un pool"""
        return self.delete(self.table_name, "id_pool", pool_id)
    
    def add_tambor_to_pool(self, pool_id: int, tambor_id: int) -> bool:
        """Agregar un tambor al pool"""
        query = "INSERT INTO compone_pool (id_pool, id_tambor, fecha_asociacion) VALUES (%s, %s, %s)"
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        result = self.execute_custom_query(query, (pool_id, tambor_id, fecha_actual), fetch=False)
        return result is not None and result > 0
    
    def remove_tambor_from_pool(self, pool_id: int, tambor_id: int) -> bool:
        """Remover un tambor del pool"""
        query = "DELETE FROM compone_pool WHERE id_pool = %s AND id_tambor = %s"
        result = self.execute_custom_query(query, (pool_id, tambor_id), fetch=False)
        return result is not None and result > 0
    
    def get_pool_with_details(self, pool_id: int) -> Optional[Dict[str, Any]]:
        """Obtener pool con detalles del analista y tambores"""
        query = """
            SELECT p.*, a.nombres as analista_nombres, a.apellidos as analista_apellidos,
                   COUNT(cp.id_tambor) as total_tambores
            FROM pool p
            LEFT JOIN analista a ON p.id_analista = a.id_analista
            LEFT JOIN compone_pool cp ON p.id_pool = cp.id_pool
            WHERE p.id_pool = %s
            GROUP BY p.id_pool, p.id_analista, p.fecha_analisis, p.num_registro, p.observaciones,
                     a.nombres, a.apellidos
        """
        result = self.execute_custom_query(query, (pool_id,))
        return result[0] if result else None
    
    def get_pools_by_analista(self, analista_id: int) -> List[Dict[str, Any]]:
        """Obtener pools de un analista específico"""
        query = """
            SELECT p.*, COUNT(cp.id_tambor) as total_tambores
            FROM pool p
            LEFT JOIN compone_pool cp ON p.id_pool = cp.id_pool
            WHERE p.id_analista = %s
            GROUP BY p.id_pool, p.id_analista, p.fecha_analisis, p.num_registro, p.observaciones
            ORDER BY p.fecha_analisis DESC
        """
        return self.execute_custom_query(query, (analista_id,)) or []
    
    def get_pools_by_date_range(self, fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """Obtener pools en un rango de fechas"""
        query = """
            SELECT p.*, a.nombres as analista_nombres, a.apellidos as analista_apellidos,
                   COUNT(cp.id_tambor) as total_tambores
            FROM pool p
            LEFT JOIN analista a ON p.id_analista = a.id_analista
            LEFT JOIN compone_pool cp ON p.id_pool = cp.id_pool
            WHERE p.fecha_analisis BETWEEN %s AND %s
            GROUP BY p.id_pool, p.id_analista, p.fecha_analisis, p.num_registro, p.observaciones,
                     a.nombres, a.apellidos
            ORDER BY p.fecha_analisis DESC
        """
        return self.execute_custom_query(query, (fecha_inicio, fecha_fin)) or [] 