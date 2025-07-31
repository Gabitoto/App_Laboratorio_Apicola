from models.base_model import BaseModel
from typing import List, Dict, Any, Optional

class Apicultor(BaseModel):
    """Modelo para la tabla apicultor"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "apicultor"
    
    def get_all_apicultores(self) -> List[Dict[str, Any]]:
        """Obtener todos los apicultores ordenados por nombre"""
        return self.get_all(self.table_name, "nombre")
    
    def get_apicultor_by_id(self, apicultor_id: int) -> Optional[Dict[str, Any]]:
        """Obtener apicultor por ID"""
        return self.get_by_id(self.table_name, "id_apicultor", apicultor_id)
    
    def create_apicultor(self, nombre: str, apellido: str) -> Optional[int]:
        """Crear un nuevo apicultor"""
        data = {
            'nombre': nombre,
            'apellido': apellido
        }
        return self.insert(self.table_name, data)
    
    def update_apicultor(self, apicultor_id: int, **kwargs) -> bool:
        """Actualizar datos de un apicultor"""
        return self.update(self.table_name, "id_apicultor", apicultor_id, kwargs)
    
    def delete_apicultor(self, apicultor_id: int) -> bool:
        """Eliminar un apicultor"""
        return self.delete(self.table_name, "id_apicultor", apicultor_id)
    
    def search_apicultores(self, search_term: str) -> List[Dict[str, Any]]:
        """Buscar apicultores por nombre o apellido"""
        query = """
            SELECT * FROM apicultor 
            WHERE LOWER(nombre) LIKE LOWER(%s) 
            OR LOWER(apellido) LIKE LOWER(%s)
            ORDER BY nombre, apellido
        """
        search_pattern = f"%{search_term}%"
        return self.execute_custom_query(query, (search_pattern, search_pattern)) or []
    
    def get_apicultores_with_tambores(self) -> List[Dict[str, Any]]:
        """Obtener apicultores que tienen tambores asociados"""
        query = """
            SELECT DISTINCT a.*, COUNT(mt.id_tambor) as total_tambores
            FROM apicultor a
            LEFT JOIN muestra_tambor mt ON a.id_apicultor = mt.id_apicultor
            GROUP BY a.id_apicultor, a.nombre, a.apellido
            HAVING COUNT(mt.id_tambor) > 0
            ORDER BY a.nombre, a.apellido
        """
        return self.execute_custom_query(query) or [] 