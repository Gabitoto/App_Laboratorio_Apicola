import streamlit as st
from typing import Dict, Any, Callable
from utils.calculators import calcular_porcentajes

class ContadorEspecies:
    """Componente para manejar contadores dinámicos de especies"""
    
    def __init__(self):
        self.especies_data = {}
    
    def render_contador_especie(self, especie: Dict[str, Any], index: int, 
                               on_change: Callable = None) -> Dict[str, Any]:
        """
        Renderizar contador para una especie específica
        
        Args:
            especie: Datos de la especie
            index: Índice único para la especie
            on_change: Función callback cuando cambia el valor
        
        Returns:
            Datos actualizados de la especie
        """
        especie_id = especie.get('id_especie')
        nombre_comun = especie.get('nombre_comun', '')
        nombre_cientifico = especie.get('nombre_cientifico', '')
        
        # Crear clave única para el estado
        key_cantidad = f"cantidad_{especie_id}_{index}"
        key_marca = f"marca_{especie_id}_{index}"
        
        # Obtener valores actuales del estado
        cantidad_actual = st.session_state.get(key_cantidad, 0)
        marca_actual = st.session_state.get(key_marca, "")
        
        # Crear contenedor para la especie
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
            
            with col1:
                st.markdown(f"**{nombre_comun}**")
                st.caption(f"*{nombre_cientifico}*")
            
            with col2:
                if st.button("➖", key=f"decrease_{especie_id}_{index}", 
                           help="Decrementar contador"):
                    nueva_cantidad = max(0, cantidad_actual - 1)
                    st.session_state[key_cantidad] = nueva_cantidad
                    if on_change:
                        on_change()
                    st.rerun()
            
            with col3:
                st.markdown(f"**{cantidad_actual}**", help="Cantidad de granos")
            
            with col4:
                if st.button("➕", key=f"increase_{especie_id}_{index}", 
                           help="Incrementar contador"):
                    nueva_cantidad = cantidad_actual + 1
                    st.session_state[key_cantidad] = nueva_cantidad
                    if on_change:
                        on_change()
                    st.rerun()
            
            with col5:
                marca_especial = st.text_input(
                    "Marca especial",
                    value=marca_actual,
                    key=key_marca,
                    placeholder="Opcional",
                    help="Marca especial para esta especie"
                )
                if marca_especial != marca_actual:
                    st.session_state[key_marca] = marca_especial
                    if on_change:
                        on_change()
        
        # Retornar datos actualizados
        return {
            'especie_id': especie_id,
            'nombre_comun': nombre_comun,
            'nombre_cientifico': nombre_cientifico,
            'cantidad_granos': cantidad_actual,
            'marca_especial': marca_especial
        }
    
    def render_contadores_especies(self, especies_seleccionadas: list, 
                                  on_change: Callable = None) -> list:
        """
        Renderizar contadores para todas las especies seleccionadas
        
        Args:
            especies_seleccionadas: Lista de especies seleccionadas
            on_change: Función callback cuando cambian los valores
        
        Returns:
            Lista con datos de todas las especies y sus contadores
        """
        if not especies_seleccionadas:
            st.info("No hay especies seleccionadas")
            return []
        
        st.subheader("Contadores de Especies")
        st.markdown("---")
        
        especies_data = []
        
        for i, especie in enumerate(especies_seleccionadas):
            especie_data = self.render_contador_especie(especie, i, on_change)
            especies_data.append(especie_data)
            
            # Separador entre especies
            if i < len(especies_seleccionadas) - 1:
                st.markdown("---")
        
        return especies_data
    
    def mostrar_resumen_contadores(self, especies_data: list):
        """
        Mostrar resumen de los contadores
        
        Args:
            especies_data: Lista con datos de especies y contadores
        """
        if not especies_data:
            return
        
        # Calcular totales
        total_granos = sum(esp.get('cantidad_granos', 0) for esp in especies_data)
        especies_con_granos = [esp for esp in especies_data if esp.get('cantidad_granos', 0) > 0]
        
        # Calcular porcentajes
        especies_con_porcentajes = calcular_porcentajes(especies_con_granos)
        
        # Mostrar resumen
        st.subheader("📊 Resumen del Análisis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Granos", f"{total_granos:,}".replace(",", "."))
        
        with col2:
            st.metric("Especies con Granos", len(especies_con_granos))
        
        with col3:
            if total_granos > 0:
                porcentaje_total = sum(esp.get('porcentaje', 0) for esp in especies_con_porcentajes)
                st.metric("Porcentaje Total", f"{porcentaje_total:.1f}%")
            else:
                st.metric("Porcentaje Total", "0%")
        
        # Mostrar tabla de resumen
        if especies_con_granos:
            st.markdown("**Detalle por Especies:**")
            
            # Crear DataFrame para mostrar
            import pandas as pd
            df_data = []
            for esp in especies_con_porcentajes:
                df_data.append({
                    'Especie': f"{esp['nombre_comun']} ({esp['nombre_cientifico']})",
                    'Granos': esp['cantidad_granos'],
                    'Porcentaje': f"{esp.get('porcentaje', 0):.2f}%",
                    'Marca Especial': esp.get('marca_especial', '')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    def validar_contadores(self, especies_data: list) -> Dict[str, Any]:
        """
        Validar los datos de los contadores
        
        Args:
            especies_data: Lista con datos de especies y contadores
        
        Returns:
            Resultado de la validación
        """
        from utils.calculators import validar_analisis
        
        return validar_analisis(especies_data)
    
    def limpiar_contadores(self):
        """Limpiar todos los contadores del estado de la sesión"""
        keys_to_remove = []
        for key in st.session_state.keys():
            if key.startswith(('cantidad_', 'marca_')):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key] 