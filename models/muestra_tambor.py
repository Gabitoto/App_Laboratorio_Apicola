from models.base_model import BaseModel
from typing import List, Dict, Any, Optional

class MuestraTambor(BaseModel):
    """Modelo para la tabla muestra_tambor"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "muestra_tambor"
    
    def get_all_tambores(self) -> List[Dict[str, Any]]:
        """Obtener todos los tambores ordenados por número de registro"""
        return self.get_all(self.table_name, "num_registro")
    
    def get_tambor_by_id(self, tambor_id: int) -> Optional[Dict[str, Any]]:
        """Obtener tambor por ID"""
        return self.get_by_id(self.table_name, "id_tambor", tambor_id)
    
    def get_tambor_by_num_registro(self, num_registro: str) -> Optional[Dict[str, Any]]:
        """Obtener tambor por número de registro"""
        return self.get_by_id(self.table_name, "num_registro", num_registro)
    
    def create_tambor(self, id_apicultor: int, num_registro: str, fecha_extraccion: str = None) -> Optional[int]:
        """Crear un nuevo tambor"""
        data = {
            'id_apicultor': id_apicultor,
            'num_registro': num_registro,
            'fecha_extraccion': fecha_extraccion
        }
        return self.insert(self.table_name, data)
    
    def update_tambor(self, tambor_id: int, **kwargs) -> bool:
        """Actualizar datos de un tambor"""
        return self.update(self.table_name, "id_tambor", tambor_id, kwargs)
    
    def delete_tambor(self, tambor_id: int) -> bool:
        """Eliminar un tambor"""
        return self.delete(self.table_name, "id_tambor", tambor_id)
    
    def get_tambores_disponibles(self) -> List[Dict[str, Any]]:
        """Obtener tambores que no están en ningún pool"""
        query = """
            SELECT mt.*, a.nombre as apicultor_nombre, a.apellido as apicultor_apellido
            FROM muestra_tambor mt
            LEFT JOIN apicultor a ON mt.id_apicultor = a.id_apicultor
            WHERE mt.id_tambor NOT IN (
                SELECT DISTINCT id_tambor FROM compone_pool
            )
            ORDER BY mt.num_registro
        """
        return self.execute_custom_query(query) or []
    
    def get_tambores_by_apicultor(self, apicultor_id: int) -> List[Dict[str, Any]]:
        """Obtener tambores de un apicultor específico"""
        query = """
            SELECT mt.*, a.nombre as apicultor_nombre, a.apellido as apicultor_apellido
            FROM muestra_tambor mt
            LEFT JOIN apicultor a ON mt.id_apicultor = a.id_apicultor
            WHERE mt.id_apicultor = %s
            ORDER BY mt.num_registro
        """
        return self.execute_custom_query(query, (apicultor_id,)) or []
    
    def get_tambores_in_pool(self, pool_id: int) -> List[Dict[str, Any]]:
        """Obtener tambores que componen un pool específico"""
        query = """
            SELECT mt.*, a.nombre as apicultor_nombre, a.apellido as apicultor_apellido
            FROM muestra_tambor mt
            LEFT JOIN apicultor a ON mt.id_apicultor = a.id_apicultor
            INNER JOIN compone_pool cp ON mt.id_tambor = cp.id_tambor
            WHERE cp.id_pool = %s
            ORDER BY mt.num_registro
        """
        return self.execute_custom_query(query, (pool_id,)) or [] 