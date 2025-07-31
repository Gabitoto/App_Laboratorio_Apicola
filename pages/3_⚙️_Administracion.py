import streamlit as st
import pandas as pd
from models.apicultor import Apicultor
from models.analista import Analista
from models.especie import Especie
from models.muestra_tambor import MuestraTambor

# Configurar página
st.set_page_config(
    page_title="Administración - Laboratorio Apícola",
    page_icon="⚙️",
    layout="wide"
)

# Título
st.title("⚙️ Administración del Sistema")
st.markdown("---")

# Inicializar modelos
apicultor_model = Apicultor()
analista_model = Analista()
especie_model = Especie()
tambor_model = MuestraTambor()

# Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs(["👨‍🌾 Apicultores", "👨‍🔬 Analistas", "🌿 Especies", "🍯 Tambores"])

# Pestaña 1: Apicultores
with tab1:
    st.header("👨‍🌾 Gestión de Apicultores")
    
    # Formulario para agregar apicultor
    with st.expander("➕ Agregar Nuevo Apicultor", expanded=False):
        with st.form("agregar_apicultor"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre *", key="apicultor_nombre")
            
            with col2:
                apellido = st.text_input("Apellido *", key="apicultor_apellido")
            
            submitted = st.form_submit_button("Agregar Apicultor", type="primary")
            
            if submitted:
                if nombre and apellido:
                    apicultor_id = apicultor_model.create_apicultor(nombre, apellido)
                    if apicultor_id:
                        st.success(f"✅ Apicultor '{nombre} {apellido}' agregado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al agregar el apicultor")
                else:
                    st.error("❌ Todos los campos son obligatorios")
    
    # Mostrar apicultores existentes
    st.subheader("📋 Apicultores Registrados")
    
    apicultores = apicultor_model.get_all_apicultores()
    
    if apicultores:
        # Crear DataFrame
        df_apicultores = pd.DataFrame(apicultores)
        df_apicultores['Nombre Completo'] = df_apicultores['nombre'] + ' ' + df_apicultores['apellido']
        df_apicultores = df_apicultores[['id_apicultor', 'Nombre Completo', 'nombre', 'apellido']]
        df_apicultores.columns = ['ID', 'Nombre Completo', 'Nombre', 'Apellido']
        
        st.dataframe(df_apicultores, use_container_width=True, hide_index=True)
        
        # Funcionalidad de eliminación
        with st.expander("🗑️ Eliminar Apicultor"):
            apicultor_a_eliminar = st.selectbox(
                "Seleccione el apicultor a eliminar:",
                options=[f"{a['id_apicultor']} - {a['nombre']} {a['apellido']}" for a in apicultores]
            )
            
            if st.button("Eliminar Apicultor", type="secondary"):
                if apicultor_a_eliminar:
                    apicultor_id = int(apicultor_a_eliminar.split(' - ')[0])
                    if apicultor_model.delete_apicultor(apicultor_id):
                        st.success("✅ Apicultor eliminado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al eliminar el apicultor")
    else:
        st.info("📝 No hay apicultores registrados. Agregue el primer apicultor usando el formulario de arriba.")

# Pestaña 2: Analistas
with tab2:
    st.header("👨‍🔬 Gestión de Analistas")
    
    # Formulario para agregar analista
    with st.expander("➕ Agregar Nuevo Analista", expanded=False):
        with st.form("agregar_analista"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombres = st.text_input("Nombres *", key="analista_nombres")
            
            with col2:
                apellidos = st.text_input("Apellidos *", key="analista_apellidos")
            
            contacto = st.text_input("Contacto (Opcional)", key="analista_contacto")
            
            submitted = st.form_submit_button("Agregar Analista", type="primary")
            
            if submitted:
                if nombres and apellidos:
                    analista_id = analista_model.create_analista(nombres, apellidos, contacto)
                    if analista_id:
                        st.success(f"✅ Analista '{nombres} {apellidos}' agregado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al agregar el analista")
                else:
                    st.error("❌ Los nombres y apellidos son obligatorios")
    
    # Mostrar analistas existentes
    st.subheader("📋 Analistas Registrados")
    
    analistas = analista_model.get_all_analistas()
    
    if analistas:
        # Crear DataFrame
        df_analistas = pd.DataFrame(analistas)
        df_analistas['Nombre Completo'] = df_analistas['nombres'] + ' ' + df_analistas['apellidos']
        df_analistas = df_analistas[['id_analista', 'Nombre Completo', 'nombres', 'apellidos', 'contacto']]
        df_analistas.columns = ['ID', 'Nombre Completo', 'Nombres', 'Apellidos', 'Contacto']
        
        st.dataframe(df_analistas, use_container_width=True, hide_index=True)
        
        # Funcionalidad de eliminación
        with st.expander("🗑️ Eliminar Analista"):
            analista_a_eliminar = st.selectbox(
                "Seleccione el analista a eliminar:",
                options=[f"{a['id_analista']} - {a['nombres']} {a['apellidos']}" for a in analistas]
            )
            
            if st.button("Eliminar Analista", type="secondary"):
                if analista_a_eliminar:
                    analista_id = int(analista_a_eliminar.split(' - ')[0])
                    if analista_model.delete_analista(analista_id):
                        st.success("✅ Analista eliminado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al eliminar el analista")
    else:
        st.info("📝 No hay analistas registrados. Agregue el primer analista usando el formulario de arriba.")

# Pestaña 3: Especies
with tab3:
    st.header("🌿 Gestión de Especies")
    
    # Formulario para agregar especie
    with st.expander("➕ Agregar Nueva Especie", expanded=False):
        with st.form("agregar_especie"):
            nombre_cientifico = st.text_input("Nombre Científico *", key="especie_cientifico")
            nombre_comun = st.text_input("Nombre Común (Opcional)", key="especie_comun")
            familia = st.text_input("Familia (Opcional)", key="especie_familia")
            
            submitted = st.form_submit_button("Agregar Especie", type="primary")
            
            if submitted:
                if nombre_cientifico:
                    especie_id = especie_model.create_especie(nombre_cientifico, nombre_comun, familia)
                    if especie_id:
                        st.success(f"✅ Especie '{nombre_cientifico}' agregada exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al agregar la especie")
                else:
                    st.error("❌ El nombre científico es obligatorio")
    
    # Mostrar especies existentes
    st.subheader("📋 Especies Registradas")
    
    especies = especie_model.get_all_especies()
    
    if especies:
        # Crear DataFrame
        df_especies = pd.DataFrame(especies)
        df_especies = df_especies[['id_especie', 'nombre_cientifico', 'nombre_comun', 'familia']]
        df_especies.columns = ['ID', 'Nombre Científico', 'Nombre Común', 'Familia']
        
        st.dataframe(df_especies, use_container_width=True, hide_index=True)
        
        # Funcionalidad de eliminación
        with st.expander("🗑️ Eliminar Especie"):
            especie_a_eliminar = st.selectbox(
                "Seleccione la especie a eliminar:",
                options=[f"{e['id_especie']} - {e['nombre_cientifico']}" for e in especies]
            )
            
            if st.button("Eliminar Especie", type="secondary"):
                if especie_a_eliminar:
                    especie_id = int(especie_a_eliminar.split(' - ')[0])
                    if especie_model.delete_especie(especie_id):
                        st.success("✅ Especie eliminada exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al eliminar la especie")
    else:
        st.info("📝 No hay especies registradas. Agregue la primera especie usando el formulario de arriba.")

# Pestaña 4: Tambores
with tab4:
    st.header("🍯 Gestión de Tambores")
    
    # Formulario para agregar tambor
    with st.expander("➕ Agregar Nuevo Tambor", expanded=False):
        with st.form("agregar_tambor"):
            # Obtener apicultores para el selector
            apicultores = apicultor_model.get_all_apicultores()
            
            if apicultores:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Selector de apicultor
                    opciones_apicultores = {f"{a['nombre']} {a['apellido']}": a['id_apicultor'] for a in apicultores}
                    apicultor_seleccionado = st.selectbox(
                        "Apicultor *",
                        options=list(opciones_apicultores.keys())
                    )
                    
                    num_registro = st.text_input("Número de Registro *", key="tambor_registro")
                
                with col2:
                    fecha_extraccion = st.date_input("Fecha de Extracción (Opcional)", key="tambor_fecha")
                
                submitted = st.form_submit_button("Agregar Tambor", type="primary")
                
                if submitted:
                    if apicultor_seleccionado and num_registro:
                        apicultor_id = opciones_apicultores[apicultor_seleccionado]
                        fecha_str = fecha_extraccion.strftime("%Y-%m-%d") if fecha_extraccion else None
                        
                        tambor_id = tambor_model.create_tambor(apicultor_id, num_registro, fecha_str)
                        if tambor_id:
                            st.success(f"✅ Tambor '{num_registro}' agregado exitosamente!")
                            st.rerun()
                        else:
                            st.error("❌ Error al agregar el tambor")
                    else:
                        st.error("❌ El apicultor y número de registro son obligatorios")
            else:
                st.warning("⚠️ Debe agregar al menos un apicultor antes de crear tambores.")
    
    # Mostrar tambores existentes
    st.subheader("📋 Tambores Registrados")
    
    tambores = tambor_model.get_all_tambores()
    
    if tambores:
        # Obtener información de apicultores para mostrar
        tambores_con_apicultor = []
        for tambor in tambores:
            apicultor = apicultor_model.get_apicultor_by_id(tambor['id_apicultor'])
            if apicultor:
                tambor['apicultor_nombre'] = f"{apicultor['nombre']} {apicultor['apellido']}"
            else:
                tambor['apicultor_nombre'] = "N/A"
            tambores_con_apicultor.append(tambor)
        
        # Crear DataFrame
        df_tambores = pd.DataFrame(tambores_con_apicultor)
        df_tambores = df_tambores[['id_tambor', 'num_registro', 'apicultor_nombre', 'fecha_extraccion']]
        df_tambores.columns = ['ID', 'Número de Registro', 'Apicultor', 'Fecha de Extracción']
        
        st.dataframe(df_tambores, use_container_width=True, hide_index=True)
        
        # Funcionalidad de eliminación
        with st.expander("🗑️ Eliminar Tambor"):
            tambor_a_eliminar = st.selectbox(
                "Seleccione el tambor a eliminar:",
                options=[f"{t['id_tambor']} - {t['num_registro']}" for t in tambores]
            )
            
            if st.button("Eliminar Tambor", type="secondary"):
                if tambor_a_eliminar:
                    tambor_id = int(tambor_a_eliminar.split(' - ')[0])
                    if tambor_model.delete_tambor(tambor_id):
                        st.success("✅ Tambor eliminado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al eliminar el tambor")
    else:
        st.info("📝 No hay tambores registrados. Agregue el primer tambor usando el formulario de arriba.")

# Sidebar con información
st.sidebar.title("ℹ️ Información")
st.sidebar.markdown("""
### 📊 Estadísticas Rápidas

**Apicultores:** {}
**Analistas:** {}
**Especies:** {}
**Tambores:** {}

### ⚠️ Notas Importantes

- Los campos marcados con * son obligatorios
- Al eliminar registros, asegúrese de que no estén siendo utilizados en análisis
- Los tambores solo pueden ser creados por apicultores registrados
""".format(
    len(apicultor_model.get_all_apicultores()),
    len(analista_model.get_all_analistas()),
    len(especie_model.get_all_especies()),
    len(tambor_model.get_all_tambores())
)) 