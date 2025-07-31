# 🐝 Sistema de Laboratorio Apícola - Análisis Palinológico

## 📋 Descripción

Sistema web desarrollado con **Streamlit** y **Python** para la gestión de análisis palinológicos en un laboratorio apícola. Permite cargar análisis de polen de miel, visualizar resultados en reportes con porcentajes, y gestionar toda la información relacionada con apicultores, analistas, especies y tambores.

## ✨ Características Principales

### 🔬 **Análisis Palinológico**
- ✅ Creación de pools de tambores para análisis
- ✅ Selector dinámico de analistas y tambores
- ✅ Contadores interactivos para granos de polen por especie
- ✅ Cálculo automático de porcentajes
- ✅ Validación en tiempo real de datos
- ✅ Marcas especiales por especie

### 📊 **Reportes y Visualizaciones**
- ✅ Filtros avanzados por fecha, analista, pool y apicultor
- ✅ Gráficos de pastel para distribución de especies
- ✅ Gráficos de barras para especies más frecuentes
- ✅ Gráficos de líneas para evolución temporal
- ✅ Exportación a Excel y CSV
- ✅ Estadísticas detalladas y métricas

### ⚙️ **Administración**
- ✅ Gestión completa de apicultores
- ✅ Gestión de analistas
- ✅ Catálogo de especies vegetales
- ✅ Gestión de tambores de miel
- ✅ Interfaz intuitiva con formularios

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.9+
- **Frontend:** Streamlit
- **Base de Datos:** PostgreSQL
- **Conexión BD:** psycopg2-binary
- **Visualización:** Plotly Express
- **Manipulación de Datos:** pandas
- **Exportación:** OpenPyXL, pandas

## 📦 Instalación

### 1. **Requisitos Previos**
- Python 3.9 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

### 2. **Clonar el Repositorio**
```bash
git clone <url-del-repositorio>
cd App_Laboratorio_Apicola
```

### 3. **Crear Entorno Virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 5. **Configurar Base de Datos**

#### A. Crear Base de Datos PostgreSQL
```sql
CREATE DATABASE laboratorio_apicola;
```

#### B. Ejecutar Script de Configuración
```bash
psql -d laboratorio_apicola -f database_setup.sql
```

#### C. Configurar Credenciales
Editar el archivo `.streamlit/secrets.toml`:
```toml
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "laboratorio_apicola"
DB_USER = "postgres"
DB_PASSWORD = "tu_password_aqui"
```

## 🚀 Ejecución

### **Iniciar la Aplicación**
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Estructura de la Base de Datos

### **Tablas Principales**

#### **apicultor**
- `id_apicultor` (SERIAL PRIMARY KEY)
- `nombre` (VARCHAR(100))
- `apellido` (VARCHAR(100))

#### **analista**
- `id_analista` (SERIAL PRIMARY KEY)
- `nombres` (VARCHAR(100))
- `apellidos` (VARCHAR(100))
- `contacto` (VARCHAR(100))

#### **muestra_tambor**
- `id_tambor` (SERIAL PRIMARY KEY)
- `id_apicultor` (INTEGER REFERENCES apicultor)
- `num_registro` (VARCHAR(50) UNIQUE)
- `fecha_extraccion` (DATE)

#### **pool**
- `id_pool` (SERIAL PRIMARY KEY)
- `id_analista` (INTEGER REFERENCES analista)
- `fecha_analisis` (DATE)
- `num_registro` (VARCHAR(50))
- `observaciones` (TEXT)

#### **especies**
- `id_especie` (SERIAL PRIMARY KEY)
- `nombre_cientifico` (VARCHAR(150))
- `nombre_comun` (VARCHAR(100))
- `familia` (VARCHAR(100))

#### **analisis_palinologico**
- `id_palinologico` (SERIAL PRIMARY KEY)
- `id_especie` (INTEGER REFERENCES especies)
- `id_pool` (INTEGER REFERENCES pool)
- `cantidad_granos` (INTEGER)
- `marca_especial` (VARCHAR(10))

#### **compone_pool**
- `id_tambor` (INTEGER REFERENCES muestra_tambor)
- `id_pool` (INTEGER REFERENCES pool)
- `fecha_asociacion` (DATE)
- PRIMARY KEY (id_tambor, id_pool)

## 📁 Estructura del Proyecto

```
App_Laboratorio_Apicola/
├── app.py                                    # Aplicación principal
├── config/                                   # Configuraciones
│   ├── __init__.py
│   ├── database.py                          # Conexión PostgreSQL
│   └── settings.py                          # Configuraciones
├── models/                                   # Modelos de datos
│   ├── __init__.py
│   ├── base_model.py                        # Clase base
│   ├── apicultor.py                         # Modelo Apicultor
│   ├── analista.py                          # Modelo Analista
│   ├── muestra_tambor.py                    # Modelo Tambores
│   ├── pool.py                              # Modelo Pool
│   ├── especie.py                           # Modelo Especies
│   └── analisis_palinologico.py             # Modelo Análisis
├── pages/                                    # Páginas de la aplicación
│   ├── __init__.py
│   ├── 1_🔬_Analisis_Palinologico.py        # Análisis
│   ├── 2_📊_Reportes_Palinologicos.py       # Reportes
│   └── 3_⚙️_Administracion.py               # Administración
├── components/                               # Componentes reutilizables
│   ├── __init__.py
│   ├── contador_especies.py                # Contadores
│   └── pool_manager.py                      # Gestor pools
├── utils/                                    # Utilidades
│   ├── __init__.py
│   ├── calculators.py                       # Cálculos
│   └── formatters.py                        # Formateo
├── .streamlit/                               # Configuración Streamlit
│   └── secrets.toml                         # Variables de entorno
├── database_setup.sql                       # Script de configuración BD
├── requirements.txt                         # Dependencias
└── README.md                                # Documentación
```

## 📖 Guía de Uso

### **1. Configuración Inicial**
1. Ejecutar la aplicación por primera vez
2. Ir a la página de **Administración**
3. Agregar al menos:
   - 1 apicultor
   - 1 analista
   - 1 especie
   - 1 tambor

### **2. Crear Análisis**
1. Ir a **Análisis Palinológico**
2. Seleccionar "Crear Nuevo Pool"
3. Elegir analista y tambores
4. Seleccionar especies para analizar
5. Usar contadores para contar granos
6. Guardar análisis

### **3. Generar Reportes**
1. Ir a **Reportes Palinológicos**
2. Aplicar filtros según necesidades
3. Visualizar gráficos y estadísticas
4. Exportar datos si es necesario

## 🔧 Configuración Avanzada

### **Variables de Entorno**
El sistema utiliza las siguientes variables de entorno (configuradas en `.streamlit/secrets.toml`):

- `DB_HOST`: Host de PostgreSQL (default: localhost)
- `DB_PORT`: Puerto de PostgreSQL (default: 5432)
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de PostgreSQL
- `DB_PASSWORD`: Contraseña de PostgreSQL

### **Configuraciones de Aplicación**
Las configuraciones se encuentran en `config/settings.py`:

- Configuraciones de base de datos
- Configuraciones de la aplicación Streamlit
- Configuraciones de reportes
- Configuraciones de validación

## 🐛 Solución de Problemas

### **Error de Conexión a Base de Datos**
1. Verificar que PostgreSQL esté ejecutándose
2. Confirmar credenciales en `.streamlit/secrets.toml`
3. Verificar que la base de datos existe
4. Ejecutar `database_setup.sql` si es necesario

### **Error de Módulos**
1. Activar el entorno virtual
2. Reinstalar dependencias: `pip install -r requirements.txt`
3. Verificar versión de Python (3.9+)

### **Error de Permisos**
1. Verificar permisos de usuario en PostgreSQL
2. Confirmar que el usuario puede crear/editar tablas

## 📈 Funcionalidades Futuras

- [ ] Exportación a PDF con ReportLab
- [ ] Gráficos 3D para visualización avanzada
- [ ] Sistema de usuarios y autenticación
- [ ] API REST para integración externa
- [ ] Dashboard en tiempo real
- [ ] Notificaciones por email
- [ ] Backup automático de datos
- [ ] Análisis estadísticos avanzados

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- Revisar la documentación
- Verificar configuración de base de datos
- Consultar logs de errores en la aplicación

---

**Desarrollado para el Laboratorio Apícola** 🐝

*Versión 1.0.0 - Compatible con estructura de base de datos existente*
