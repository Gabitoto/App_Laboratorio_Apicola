from models.base_model import BaseModel
from typing import List, Dict, Any, Optional

class Analista(BaseModel):
    """Modelo para la tabla analista"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "analista"
    
    def get_all_analistas(self) -> List[Dict[str, Any]]:
        """Obtener todos los analistas ordenados por nombres"""
        return self.get_all(self.table_name, "nombres")
    
    def get_analista_by_id(self, analista_id: int) -> Optional[Dict[str, Any]]:
        """Obtener analista por ID"""
        return self.get_by_id(self.table_name, "id_analista", analista_id)
    
    def create_analista(self, nombres: str, apellidos: str, contacto: str = None) -> Optional[int]:
        """Crear un nuevo analista"""
        data = {
            'nombres': nombres,
            'apellidos': apellidos,
            'contacto': contacto
        }
        return self.insert(self.table_name, data)
    
    def update_analista(self, analista_id: int, **kwargs) -> bool:
        """Actualizar datos de un analista"""
        return self.update(self.table_name, "id_analista", analista_id, kwargs)
    
    def delete_analista(self, analista_id: int) -> bool:
        """Eliminar un analista"""
        return self.delete(self.table_name, "id_analista", analista_id)
    
    def get_analistas_with_analisis(self) -> List[Dict[str, Any]]:
        """Obtener analistas que han realizado análisis"""
        query = """
            SELECT DISTINCT a.*, COUNT(p.id_pool) as total_analisis
            FROM analista a
            LEFT JOIN pool p ON a.id_analista = p.id_analista
            LEFT JOIN analisis_palinologico ap ON p.id_pool = ap.id_pool
            GROUP BY a.id_analista, a.nombres, a.apellidos, a.contacto
            HAVING COUNT(ap.id_palinologico) > 0
            ORDER BY a.nombres, a.apellidos
        """
        return self.execute_custom_query(query) or []
    
    def get_analista_full_name(self, analista_id: int) -> str:
        """Obtener nombre completo del analista"""
        analista = self.get_analista_by_id(analista_id)
        if analista:
            return f"{analista['nombres']} {analista['apellidos']}"
        return "Analista no encontrado" 