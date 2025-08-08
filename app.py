import streamlit as st
import sys
import traceback
from config.settings import APP_CONFIG
from config.database import get_database_connection

# Configurar manejo de errores global
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    st.error(f"Error no manejado: {exc_value}")
    st.error(f"Traceback: {traceback.format_exception(exc_type, exc_value, exc_traceback)}")

sys.excepthook = handle_exception

# Configurar la aplicación
st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
)

# Título principal
st.title("🐝 Laboratorio Apícola - Sistema de Análisis Palinológico")
st.markdown("---")

# Verificar conexión a la base de datos
@st.cache_resource
def verificar_conexion_db():
    """Verificar la conexión a la base de datos"""
    try:
        db = get_database_connection()
        # Intentar una consulta simple
        result = db.execute_query("SELECT 1")
        return True if result else False
    except Exception as e:
        st.error(f"❌ Error de conexión a la base de datos: {str(e)}")
        return False

# Verificar conexión
if not verificar_conexion_db():
    st.error("""
    ### ❌ Error de Conexión a la Base de Datos
    
    **Posibles causas:**
    1. PostgreSQL no está ejecutándose
    2. Las credenciales de la base de datos son incorrectas
    3. La base de datos no existe
    
    **Solución:**
    1. Verifique que PostgreSQL esté instalado y ejecutándose
    2. Configure las variables de entorno en `.streamlit/secrets.toml`:
    
    ```toml
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "laboratorio_apicola"
    DB_USER = "postgres"
    DB_PASSWORD = "tu_password"
    ```
    
    3. Cree la base de datos si no existe:
    ```sql
    CREATE DATABASE laboratorio_apicola;
    ```
    """)
    st.stop()

# Página principal
st.header("🏠 Página Principal")
st.markdown("""
### Bienvenido al Sistema de Laboratorio Apícola

Este sistema permite gestionar análisis palinológicos de miel, incluyendo:

🔬 **Análisis Palinológico**
- Crear pools de tambores
- Realizar análisis de especies
- Contar granos de polen
- Calcular porcentajes automáticamente

📊 **Reportes Palinológicos**
- Generar reportes con filtros
- Visualizaciones gráficas
- Exportación a Excel y CSV
- Estadísticas detalladas

⚙️ **Administración**
- Gestión de apicultores
- Gestión de analistas
- Gestión de especies
- Gestión de tambores

### 🚀 Comenzar

Para comenzar a usar el sistema:

1. **Configure los datos maestros** en la página de Administración
2. **Cree pools** de tambores para análisis
3. **Realice análisis palinológicos** con contadores dinámicos
4. **Genere reportes** con visualizaciones

### 📋 Requisitos del Sistema

- **Base de datos:** PostgreSQL
- **Python:** 3.9+
- **Dependencias:** Ver `requirements.txt`

### 🔧 Configuración

El sistema utiliza las siguientes configuraciones:

- **Base de datos:** Configurada en `config/settings.py`
- **Variables de entorno:** Archivo `.streamlit/secrets.toml`
- **Estructura:** Organizada en módulos y componentes

### 📚 Estructura del Proyecto

```
App_Laboratorio_Apicola/
├── app.py                                    # Aplicación principal
├── config/                                   # Configuraciones
│   ├── database.py                          # Conexión PostgreSQL
│   └── settings.py                          # Configuraciones
├── models/                                   # Modelos de datos
│   ├── base_model.py                        # Clase base
│   ├── apicultor.py                         # Modelo Apicultor
│   ├── analista.py                          # Modelo Analista
│   ├── muestra_tambor.py                    # Modelo Tambores
│   ├── pool.py                              # Modelo Pool
│   ├── especie.py                           # Modelo Especies
│   └── analisis_palinologico.py             # Modelo Análisis
├── pages/                                    # Páginas de la aplicación
│   ├── 1_🔬_Analisis_Palinologico.py        # Análisis
│   ├── 2_📊_Reportes_Palinologicos.py       # Reportes
│   └── 3_⚙️_Administracion.py               # Administración
├── components/                               # Componentes reutilizables
│   ├── contador_especies.py                # Contadores
│   └── pool_manager.py                      # Gestor pools
├── utils/                                    # Utilidades
│   ├── calculators.py                       # Cálculos
│   └── formatters.py                        # Formateo
└── requirements.txt                         # Dependencias
```

### 🐝 Funcionalidades Principales

#### Análisis Palinológico
- **Selector de Analista:** Dropdown con analistas disponibles
- **Selector de Tambores:** Multiselect de tambores para crear pools
- **Contadores Dinámicos:** Botones +/- para contar granos por especie
- **Cálculo Automático:** Porcentajes calculados automáticamente
- **Validación:** Verificación de datos antes de guardar

#### Reportes
- **Filtros Avanzados:** Por fecha, analista, pool, apicultor
- **Visualizaciones:** Gráficos de pastel, barras y líneas
- **Exportación:** Excel y CSV con datos completos
- **Estadísticas:** Métricas y análisis detallados

#### Administración
- **CRUD Completo:** Crear, leer, actualizar, eliminar
- **Gestión de Maestros:** Apicultores, analistas, especies, tambores
- **Interfaz Intuitiva:** Formularios y tablas organizadas

### 📊 Base de Datos

El sistema utiliza las siguientes tablas principales:

- **apicultor:** Información de apicultores
- **analista:** Información de analistas
- **muestra_tambor:** Tambores de miel
- **pool:** Grupos de tambores para análisis
- **especies:** Catálogo de especies vegetales
- **analisis_palinologico:** Resultados de análisis
- **compone_pool:** Relación entre pools y tambores

### 🔍 Navegación

Use la barra lateral para navegar entre las diferentes secciones:

- **🔬 Análisis Palinológico:** Realizar análisis
- **📊 Reportes Palinológicos:** Generar reportes
- **⚙️ Administración:** Gestionar datos maestros

---

**Desarrollado para el Laboratorio Apícola** 🐝
""")

# Sidebar con información del sistema
st.sidebar.title("ℹ️ Información del Sistema")

# Estado de la conexión
if verificar_conexion_db():
    st.sidebar.success("✅ Conexión a BD: Activa")
else:
    st.sidebar.error("❌ Conexión a BD: Error")

# Información del sistema
st.sidebar.markdown("""
### 📊 Estadísticas Rápidas

Para ver estadísticas detalladas, visite la página de **Reportes Palinológicos**.

### 🔧 Configuración

- **Versión:** 1.0.0
- **Base de Datos:** PostgreSQL
- **Framework:** Streamlit
- **Lenguaje:** Python 3.9+

### 📞 Soporte

Para soporte técnico o consultas:
- Revisar la documentación
- Verificar configuración de BD
- Consultar logs de errores
""")

# Footer
st.markdown("---")
st.markdown("*Sistema de Laboratorio Apícola - Versión 1.0.0*")
