from config.database import get_db
from typing import List, Dict, Any, Optional

class BaseModel:
    """Clase base para todos los modelos de la aplicación"""
    
    def __init__(self):
        self.db = get_db()
    
    def get_all(self, table_name: str, order_by: str = None) -> List[Dict[str, Any]]:
        """Obtener todos los registros de una tabla"""
        query = f"SELECT * FROM {table_name}"
        if order_by:
            query += f" ORDER BY {order_by}"
        return self.db.execute_query(query) or []
    
    def get_by_id(self, table_name: str, id_field: str, id_value: Any) -> Optional[Dict[str, Any]]:
        """Obtener un registro por ID"""
        query = f"SELECT * FROM {table_name} WHERE {id_field} = %s"
        result = self.db.execute_query(query, (id_value,))
        return result[0] if result else None
    
    def insert(self, table_name: str, data: Dict[str, Any], id_field: str = None) -> Optional[int]:
        """Insertar un nuevo registro"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        
        # Determinar el nombre del campo ID
        if id_field is None:
            # Mapeo de nombres de tabla a campos ID
            id_field_mapping = {
                'pool': 'id_pool',
                'analista': 'id_analista',
                'apicultor': 'id_apicultor',
                'especie': 'id_especie',
                'muestra_tambor': 'id_tambor',
                'analisis_palinologico': 'id_palinologico'
            }
            id_field = id_field_mapping.get(table_name, 'id')
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING {id_field}"
        
        result = self.db.execute_query(query, tuple(data.values()))
        return result[0][id_field] if result else None
    
    def update(self, table_name: str, id_field: str, id_value: Any, data: Dict[str, Any]) -> bool:
        """Actualizar un registro existente"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_field} = %s"
        
        values = list(data.values()) + [id_value]
        result = self.db.execute_query(query, tuple(values), fetch=False)
        return result is not None and result > 0
    
    def delete(self, table_name: str, id_field: str, id_value: Any) -> bool:
        """Eliminar un registro"""
        query = f"DELETE FROM {table_name} WHERE {id_field} = %s"
        result = self.db.execute_query(query, (id_value,), fetch=False)
        return result is not None and result > 0
    
    def execute_custom_query(self, query: str, params: tuple = None, fetch: bool = True) -> Any:
        """Ejecutar una consulta personalizada"""
        return self.db.execute_query(query, params, fetch)
    
    def execute_many(self, query: str, params_list: List[tuple]) -> Optional[int]:
        """Ejecutar múltiples consultas"""
        return self.db.execute_many(query, params_list) 