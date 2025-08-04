import psycopg2
import psycopg2.extras
from psycopg2 import pool
import streamlit as st
from config.settings import DATABASE_CONFIG

class DatabaseConnection:
    """Clase para manejar la conexión a la base de datos PostgreSQL"""
    
    def __init__(self):
        self.connection_pool = None
        self._create_connection_pool()
    
    def _create_connection_pool(self):
        """Crear pool de conexiones a la base de datos"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=DATABASE_CONFIG['host'],
                port=DATABASE_CONFIG['port'],
                database=DATABASE_CONFIG['database'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password']
            )
        except Exception as e:
            st.error(f"Error al conectar con la base de datos: {str(e)}")
            st.info("Verifica que PostgreSQL esté ejecutándose y las credenciales sean correctas.")
    
    def get_connection(self):
        """Obtener una conexión del pool"""
        if self.connection_pool:
            return self.connection_pool.getconn()
        return None
    
    def return_connection(self, connection):
        """Devolver una conexión al pool"""
        if self.connection_pool and connection:
            self.connection_pool.putconn(connection)
    
    def execute_query(self, query, params=None, fetch=True):
        """Ejecutar una consulta SQL"""
        connection = None
        try:
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(query, params)
                
                if fetch:
                    result = cursor.fetchall()
                    # Hacer commit para confirmar la transacción
                    connection.commit()
                else:
                    connection.commit()
                    result = cursor.rowcount
                
                cursor.close()
                return result
        except Exception as e:
            if connection:
                connection.rollback()
            st.error(f"Error en la consulta: {str(e)}")
            return None
        finally:
            if connection:
                self.return_connection(connection)
    
    def execute_many(self, query, params_list):
        """Ejecutar múltiples consultas"""
        connection = None
        try:
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor()
                cursor.executemany(query, params_list)
                connection.commit()
                result = cursor.rowcount
                cursor.close()
                return result
        except Exception as e:
            if connection:
                connection.rollback()
            st.error(f"Error en la ejecución múltiple: {str(e)}")
            return None
        finally:
            if connection:
                self.return_connection(connection)
    
    def close_pool(self):
        """Cerrar el pool de conexiones"""
        if self.connection_pool:
            self.connection_pool.closeall()

# Instancia global de la conexión
@st.cache_resource
def get_database_connection():
    """Obtener instancia de conexión a la base de datos (cached)"""
    return DatabaseConnection()

# Función helper para obtener conexión
def get_db():
    """Función helper para obtener la conexión a la base de datos"""
    return get_database_connection()
