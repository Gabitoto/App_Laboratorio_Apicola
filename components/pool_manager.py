import streamlit as st
from typing import List, Dict, Any, Optional
from models.analista import Analista
from models.muestra_tambor import MuestraTambor
from models.pool import Pool
from datetime import datetime

class PoolManager:
    """Componente para gestionar la creación de pools"""
    
    def __init__(self):
        self.analista_model = Analista()
        self.tambor_model = MuestraTambor()
        self.pool_model = Pool()
    
    def render_selector_analista(self):
        """Renderizar selector de analista"""
        st.subheader("👨‍🔬 Seleccionar Analista")
        
        # Obtener analistas
        analistas = self.analista_model.get_all_analistas()
        
        if not analistas:
            st.warning("No hay analistas registrados. Por favor, agregue analistas en la página de Administración.")
            return None
        
        # Crear opciones para el selector
        opciones_analistas = {}
        for analista in analistas:
            nombre_completo = f"{analista['nombres']} {analista['apellidos']}"
            opciones_analistas[nombre_completo] = analista['id_analista']
        
        # Selector de analista
        analista_seleccionado = st.selectbox(
            "Seleccione el analista que realizará el análisis:",
            options=list(opciones_analistas.keys()),
            index=0
        )
        
        return opciones_analistas[analista_seleccionado] if analista_seleccionado else None
    
    def render_selector_tambores(self):
        """Renderizar selector de tambores"""
        st.subheader("🍯 Seleccionar Tambores")
        
        # Obtener tambores disponibles
        tambores_disponibles = self.tambor_model.get_tambores_disponibles()
        
        if not tambores_disponibles:
            st.warning("No hay tambores disponibles. Por favor, agregue tambores en la página de Administración.")
            return []
        
        # Crear opciones para el multiselect
        opciones_tambores = {}
        for tambor in tambores_disponibles:
            nombre_apicultor = f"{tambor['apicultor_nombre']} {tambor['apicultor_apellido']}"
            opcion = f"{tambor['num_registro']} - {nombre_apicultor}"
            opciones_tambores[opcion] = tambor['id_tambor']
        
        # Multiselect de tambores
        tambores_seleccionados = st.multiselect(
            "Seleccione los tambores para el análisis:",
            options=list(opciones_tambores.keys()),
            help="Puede seleccionar múltiples tambores para crear un pool"
        )
        
        return [opciones_tambores[t] for t in tambores_seleccionados]
    
    def render_fecha_analisis(self):
        """Renderizar selector de fecha de análisis"""
        st.subheader("📅 Fecha de Análisis")
        
        fecha_analisis = st.date_input(
            "Seleccione la fecha del análisis:",
            value=datetime.now().date(),
            help="Fecha en que se realizará el análisis palinológico"
        )
        
        return fecha_analisis.strftime("%Y-%m-%d") if fecha_analisis else None
    
    def render_observaciones_pool(self):
        """Renderizar campo de observaciones"""
        st.subheader("📝 Observaciones (Opcional)")
        
        observaciones = st.text_area(
            "Observaciones adicionales sobre el pool:",
            placeholder="Ingrese observaciones sobre el análisis, condiciones especiales, etc.",
            height=100
        )
        
        return observaciones if observaciones.strip() else None
    
    def crear_pool(self, id_analista: int, fecha_analisis: str, tambores_ids: List[int], observaciones: str = None):
        """Crear un nuevo pool con los tambores seleccionados"""
        try:
            # Crear el pool
            pool_id = self.pool_model.create_pool(
                id_analista=id_analista,
                fecha_analisis=fecha_analisis,
                observaciones=observaciones
            )
            
            if not pool_id:
                st.error("Error al crear el pool")
                return None
            
            # Agregar tambores al pool
            tambores_agregados = 0
            for tambor_id in tambores_ids:
                if self.pool_model.add_tambor_to_pool(pool_id, tambor_id):
                    tambores_agregados += 1
            
            if tambores_agregados != len(tambores_ids):
                st.warning(f"Se agregaron {tambores_agregados} de {len(tambores_ids)} tambores al pool")
            
            return pool_id
            
        except Exception as e:
            st.error(f"Error al crear el pool: {str(e)}")
            return None
    
    def mostrar_resumen_pool(self, pool_id: int):
        """Mostrar resumen del pool creado"""
        pool_info = self.pool_model.get_pool_with_details(pool_id)
        tambores = self.tambor_model.get_tambores_in_pool(pool_id)
        
        if pool_info:
            st.success("✅ Pool creado exitosamente!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("ID del Pool", pool_id)
                st.metric("Analista", f"{pool_info['analista_nombres']} {pool_info['analista_apellidos']}")
            
            with col2:
                st.metric("Fecha de Análisis", pool_info['fecha_analisis'])
                st.metric("Tambores", len(tambores))
            
            if observaciones := pool_info.get('observaciones'):
                st.info(f"**Observaciones:** {observaciones}")
            
            # Mostrar tambores
            if tambores:
                st.subheader("Tambores en el Pool:")
                for tambor in tambores:
                    st.write(f"• {tambor['num_registro']} - {tambor['apicultor_nombre']} {tambor['apicultor_apellido']}")
    
    def render_creacion_pool_completa(self):
        """Renderizar el formulario completo de creación de pool"""
        st.header("🏗️ Crear Nuevo Pool de Análisis")
        st.markdown("---")
        
        with st.form("crear_pool_form"):
            # Selector de analista
            id_analista = self.render_selector_analista()
            
            # Selector de tambores
            tambores_ids = self.render_selector_tambores()
            
            # Fecha de análisis
            fecha_analisis = self.render_fecha_analisis()
            
            # Observaciones
            observaciones = self.render_observaciones_pool()
            
            # Botón de envío
            submitted = st.form_submit_button("🏗️ Crear Pool", type="primary")
            
            if submitted:
                if not id_analista:
                    st.error("Debe seleccionar un analista")
                    return None
                
                if not tambores_ids:
                    st.error("Debe seleccionar al menos un tambor")
                    return None
                
                if not fecha_analisis:
                    st.error("Debe seleccionar una fecha de análisis")
                    return None
                
                # Crear el pool
                pool_id = self.crear_pool(id_analista, fecha_analisis, tambores_ids, observaciones)
                
                if pool_id:
                    self.mostrar_resumen_pool(pool_id)
                    return pool_id
        
        return None 