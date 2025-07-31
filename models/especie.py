from models.base_model import BaseModel
from typing import List, Dict, Any, Optional

class Especie(BaseModel):
    """Modelo para la tabla especies"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "especies"
    
    def get_all_especies(self) -> List[Dict[str, Any]]:
        """Obtener todas las especies ordenadas por nombre común"""
        return self.get_all(self.table_name, "nombre_comun")
    
    def get_especie_by_id(self, especie_id: int) -> Optional[Dict[str, Any]]:
        """Obtener especie por ID"""
        return self.get_by_id(self.table_name, "id_especie", especie_id)
    
    def create_especie(self, nombre_cientifico: str, nombre_comun: str = None, familia: str = None) -> Optional[int]:
        """Crear una nueva especie"""
        data = {
            'nombre_cientifico': nombre_cientifico,
            'nombre_comun': nombre_comun,
            'familia': familia
        }
        return self.insert(self.table_name, data)
    
    def update_especie(self, especie_id: int, **kwargs) -> bool:
        """Actualizar datos de una especie"""
        return self.update(self.table_name, "id_especie", especie_id, kwargs)
    
    def delete_especie(self, especie_id: int) -> bool:
        """Eliminar una especie"""
        return self.delete(self.table_name, "id_especie", especie_id)
    
    def search_especies(self, search_term: str) -> List[Dict[str, Any]]:
        """Buscar especies por nombre común o científico"""
        query = """
            SELECT * FROM especies 
            WHERE LOWER(nombre_comun) LIKE LOWER(%s) 
            OR LOWER(nombre_cientifico) LIKE LOWER(%s)
            ORDER BY nombre_comun
        """
        search_pattern = f"%{search_term}%"
        return self.execute_custom_query(query, (search_pattern, search_pattern)) or []
    
    def get_especies_by_familia(self, familia: str) -> List[Dict[str, Any]]:
        """Obtener especies por familia"""
        query = """
            SELECT * FROM especies 
            WHERE LOWER(familia) = LOWER(%s)
            ORDER BY nombre_comun
        """
        return self.execute_custom_query(query, (familia,)) or []
    
    def get_especies_with_analisis(self) -> List[Dict[str, Any]]:
        """Obtener especies que han sido analizadas"""
        query = """
            SELECT DISTINCT e.*, COUNT(ap.id_palinologico) as total_analisis
            FROM especies e
            INNER JOIN analisis_palinologico ap ON e.id_especie = ap.id_especie
            GROUP BY e.id_especie, e.nombre_cientifico, e.nombre_comun, e.familia
            ORDER BY e.nombre_comun
        """
        return self.execute_custom_query(query) or []
    
    def get_especie_full_name(self, especie_id: int) -> str:
        """Obtener nombre completo de la especie (común + científico)"""
        especie = self.get_especie_by_id(especie_id)
        if especie:
            nombre_comun = especie.get('nombre_comun', '')
            nombre_cientifico = especie.get('nombre_cientifico', '')
            if nombre_comun:
                return f"{nombre_comun} ({nombre_cientifico})"
            else:
                return nombre_cientifico
        return "Especie no encontrada" 