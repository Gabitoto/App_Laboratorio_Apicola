import os
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno
load_dotenv()

def _get_config_value(key: str, default_value: str) -> str:
    """Obtiene un valor de configuración priorizando st.secrets, luego variables de entorno y por último el default."""
    # 1) st.secrets (Streamlit Cloud / local .streamlit/secrets.toml)
    secret_value = None
    try:
        # st.secrets puede no existir en ciertos contextos (tests)
        secret_value = st.secrets[key] if hasattr(st, 'secrets') and key in st.secrets else None
    except Exception:
        secret_value = None

    # 2) Variables de entorno
    env_value = os.getenv(key, None)

    if secret_value not in (None, ""):
        return str(secret_value)
    if env_value not in (None, ""):
        return env_value
    return default_value

# Configuraciones de la base de datos
DATABASE_CONFIG = {
    'host': _get_config_value('DB_HOST', 'localhost'),
    'port': _get_config_value('DB_PORT', '5432'),
    'database': _get_config_value('DB_NAME', 'laboratorio_apicola'),
    'user': _get_config_value('DB_USER', 'postgres'),
    'password': _get_config_value('DB_PASSWORD', ''),
    # Neon requiere TLS; usar "require" en producción/Neon
    'sslmode': _get_config_value('DB_SSLMODE', 'prefer'),
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
    'min_granos_recomendado': 100,  # Ya no es obligatorio, solo recomendado
} 