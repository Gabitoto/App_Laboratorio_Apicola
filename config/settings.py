import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuraciones de la base de datos
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'laboratorio_apicola'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
}

# Configuraciones de la aplicación
APP_CONFIG = {
    'title': 'Laboratorio Apícola - Análisis Palinológico',
    'page_icon': '🐝',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
}

# Configuraciones de reportes
REPORT_CONFIG = {
    'default_filename': 'analisis_palinologico',
    'pdf_orientation': 'portrait',
    'excel_sheet_name': 'Análisis Palinológico',
}

# Configuraciones de validación
VALIDATION_CONFIG = {
    'max_especies_per_analisis': 50,
    'max_granos_per_especie': 10000,
    'min_granos_total': 100,
} 