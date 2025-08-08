import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models.analisis_palinologico import AnalisisPalinologico
from models.pool import Pool
from models.analista import Analista
from models.apicultor import Apicultor
from utils.calculators import calcular_estadisticas_analisis
from utils.formatters import formatear_fecha, crear_dataframe_analisis

# Configurar página
st.set_page_config(
    page_title="Reportes Palinológicos - Laboratorio Apícola",
    page_icon="📊",
    layout="wide"
)

# Título de la página
st.title("📊 Reportes Palinológicos")
st.markdown("---")

# Inicializar modelos
analisis_model = AnalisisPalinologico()
pool_model = Pool()
analista_model = Analista()
apicultor_model = Apicultor()

# Sidebar para filtros
st.sidebar.title("🔍 Filtros de Reporte")

# Filtro por fecha
st.sidebar.subheader("📅 Rango de Fechas")
fecha_inicio = st.sidebar.date_input(
    "Fecha de inicio:",
    value=(datetime.now() - timedelta(days=30)).date(),
    help="Fecha de inicio para filtrar análisis"
)

fecha_fin = st.sidebar.date_input(
    "Fecha de fin:",
    value=datetime.now().date(),
    help="Fecha de fin para filtrar análisis"
)

# Filtro por analista
st.sidebar.subheader("👨‍🔬 Analista")
analistas = analista_model.get_all_analistas()
opciones_analistas = ["Todos los analistas"] + [f"{a['nombres']} {a['apellidos']}" for a in analistas]
analista_seleccionado = st.sidebar.selectbox(
    "Seleccionar analista:",
    options=opciones_analistas,
    help="Filtrar por analista específico"
)

# Filtro por pool
st.sidebar.subheader("🛢️ Pool")
pools = pool_model.get_all_pools()
opciones_pools = ["Todos los pools"] + [f"Pool #{p['id_pool']}" for p in pools]
pool_seleccionado = st.sidebar.selectbox(
    "Seleccionar pool:",
    options=opciones_pools,
    help="Filtrar por pool específico"
)

# Filtro por apicultor
st.sidebar.subheader("👨‍🌾 Apicultor")
apicultores = apicultor_model.get_all_apicultores()
opciones_apicultores = ["Todos los apicultores"] + [f"{a['nombre']} {a['apellido']}" for a in apicultores]
apicultor_seleccionado = st.sidebar.selectbox(
    "Seleccionar apicultor:",
    options=opciones_apicultores,
    help="Filtrar por apicultor específico"
)

# Botón para aplicar filtros
aplicar_filtros = st.sidebar.button("🔍 Aplicar Filtros", type="primary")

# Contenido principal
if aplicar_filtros or 'filtros_aplicados' not in st.session_state:
    st.session_state['filtros_aplicados'] = True
    
    # Aplicar filtros
    fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
    fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")
    
    # Obtener análisis filtrados
    analisis_filtrados = analisis_model.get_analisis_by_date_range(fecha_inicio_str, fecha_fin_str)
    
    # Aplicar filtros adicionales
    if analista_seleccionado != "Todos los analistas":
        analista_id = None
        for analista in analistas:
            if f"{analista['nombres']} {analista['apellidos']}" == analista_seleccionado:
                analista_id = analista['id_analista']
                break
        
        if analista_id:
            analisis_filtrados = [a for a in analisis_filtrados if a.get('id_analista') == analista_id]
    
    if pool_seleccionado != "Todos los pools":
        pool_id = int(pool_seleccionado.split("#")[1])
        analisis_filtrados = [a for a in analisis_filtrados if a.get('id_pool') == pool_id]
    
    if apicultor_seleccionado != "Todos los apicultores":
        apicultor_id = None
        for apicultor in apicultores:
            if f"{apicultor['nombre']} {apicultor['apellido']}" == apicultor_seleccionado:
                apicultor_id = apicultor['id_apicultor']
                break
        
        if apicultor_id:
            # Filtrar por apicultor (necesitamos obtener los pools del apicultor)
            pools_apicultor = pool_model.get_pools_by_apicultor(apicultor_id)
            pool_ids = [p['id_pool'] for p in pools_apicultor]
            analisis_filtrados = [a for a in analisis_filtrados if a.get('id_pool') in pool_ids]
    
    # Mostrar resultados
    st.header("📈 Resultados del Reporte")
    
    if not analisis_filtrados:
        st.info("No se encontraron análisis con los filtros aplicados.")
    else:
        # Métricas generales
        st.subheader("📊 Métricas Generales")
        
        total_analisis = len(set(a['id_pool'] for a in analisis_filtrados))
        total_especies = len(set(a['id_especie'] for a in analisis_filtrados))
        total_granos = sum(a.get('cantidad_granos', 0) for a in analisis_filtrados)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Análisis", total_analisis)
        
        with col2:
            st.metric("Total de Especies", total_especies)
        
        with col3:
            st.metric("Total de Granos", f"{total_granos:,}".replace(",", "."))
        
        with col4:
            if total_analisis > 0:
                promedio_granos = total_granos / total_analisis
                st.metric("Promedio Granos/Analisis", f"{promedio_granos:.0f}")
            else:
                st.metric("Promedio Granos/Analisis", "0")
        
        st.markdown("---")
        
        # Tabla de resumen
        st.subheader("📋 Tabla de Resumen")
        
        # Crear DataFrame para mostrar
        df_data = []
        for analisis in analisis_filtrados:
            df_data.append({
                'Pool ID': analisis.get('id_pool'),
                'Fecha': formatear_fecha(analisis.get('fecha_analisis', '')),
                'Analista': f"{analisis.get('analista_nombres', '')} {analisis.get('analista_apellidos', '')}",
                'Especie': f"{analisis.get('nombre_comun', '')} ({analisis.get('nombre_cientifico', '')})",
                'Granos': analisis.get('cantidad_granos', 0),
                'Porcentaje': f"{analisis.get('porcentaje', 0):.2f}%"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Gráficos
        st.subheader("📊 Visualizaciones")
        
        # Gráfico 1: Distribución de especies
        if analisis_filtrados:
            # Agrupar por especie
            especies_data = {}
            for analisis in analisis_filtrados:
                especie_key = f"{analisis.get('nombre_comun', '')} ({analisis.get('nombre_cientifico', '')})"
                if especie_key not in especies_data:
                    especies_data[especie_key] = 0
                especies_data[especie_key] += analisis.get('cantidad_granos', 0)
            
            # Crear gráfico de pastel
            if especies_data:
                fig_pie = px.pie(
                    values=list(especies_data.values()),
                    names=list(especies_data.keys()),
                    title="Distribución de Especies por Cantidad de Granos"
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
        
        # Gráfico 2: Análisis por fecha
        if analisis_filtrados:
            # Agrupar por fecha
            fechas_data = {}
            for analisis in analisis_filtrados:
                fecha = analisis.get('fecha_analisis', '')
                if fecha not in fechas_data:
                    fechas_data[fecha] = 0
                fechas_data[fecha] += analisis.get('cantidad_granos', 0)
            
            if fechas_data:
                fig_line = px.line(
                    x=list(fechas_data.keys()),
                    y=list(fechas_data.values()),
                    title="Evolución de Granos por Fecha",
                    labels={'x': 'Fecha', 'y': 'Total de Granos'}
                )
                st.plotly_chart(fig_line, use_container_width=True)
        
        # Gráfico 3: Top 10 especies
        if analisis_filtrados:
            # Agrupar por especie y calcular totales
            especies_totales = {}
            for analisis in analisis_filtrados:
                especie_key = f"{analisis.get('nombre_comun', '')} ({analisis.get('nombre_cientifico', '')})"
                if especie_key not in especies_totales:
                    especies_totales[especie_key] = 0
                especies_totales[especie_key] += analisis.get('cantidad_granos', 0)
            
            # Obtener top 10
            top_especies = sorted(especies_totales.items(), key=lambda x: x[1], reverse=True)[:10]
            
            if top_especies:
                fig_bar = px.bar(
                    x=[esp[1] for esp in top_especies],
                    y=[esp[0] for esp in top_especies],
                    orientation='h',
                    title="Top 10 Especies por Cantidad de Granos",
                    labels={'x': 'Total de Granos', 'y': 'Especie'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        # Análisis detallado por pool
        st.subheader("🔍 Análisis Detallado por Pool")
        
        # Obtener pools únicos
        pools_unicos = list(set(a['id_pool'] for a in analisis_filtrados))
        
        for pool_id in pools_unicos:
            analisis_pool = [a for a in analisis_filtrados if a['id_pool'] == pool_id]
            
            if analisis_pool:
                # Obtener información del pool
                pool_info = pool_model.get_pool_with_details(pool_id)
                
                with st.expander(f"Pool #{pool_id} - {analisis_pool[0].get('fecha_analisis', '')}"):
                    if pool_info:
                        st.markdown(f"**Analista:** {pool_info['analista_nombres']} {pool_info['analista_apellidos']}")
                        st.markdown(f"**Fecha:** {formatear_fecha(pool_info['fecha_analisis'])}")
                        st.markdown(f"**Total de Tambores:** {pool_info['total_tambores']}")
                    
                    # Mostrar análisis de especies
                    df_pool = crear_dataframe_analisis(analisis_pool)
                    st.dataframe(df_pool, use_container_width=True, hide_index=True)
                    
                    # Calcular estadísticas del pool
                    estadisticas = calcular_estadisticas_analisis(analisis_pool)
                    if estadisticas:
                        st.markdown("**Estadísticas del Pool:**")
                        st.markdown(f"- Total de Granos: {estadisticas['total_granos']:,}")
                        st.markdown(f"- Total de Especies: {estadisticas['total_especies']}")
                        st.markdown(f"- Diversidad (Shannon): {estadisticas['diversidad_shannon']:.3f}")
                        
                        if estadisticas['especie_dominante']:
                            especie_dom = estadisticas['especie_dominante']
                            st.markdown(f"- Especie Dominante: {especie_dom.get('nombre_comun', 'N/A')} ({especie_dom.get('porcentaje', 0):.2f}%)")
        
        st.markdown("---")
        
        # Botones de exportación
        st.subheader("📤 Exportar Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Exportar a Excel", use_container_width=True):
                # Crear DataFrame para exportar
                df_export = pd.DataFrame(df_data)
                
                # Generar nombre de archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reporte_palinologico_{timestamp}.xlsx"
                
                # Exportar
                df_export.to_excel(filename, index=False)
                
                # Descargar archivo
                with open(filename, "rb") as file:
                    st.download_button(
                        label="📥 Descargar Excel",
                        data=file.read(),
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        
        with col2:
            if st.button("📄 Exportar a CSV", use_container_width=True):
                # Crear DataFrame para exportar
                df_export = pd.DataFrame(df_data)
                
                # Generar nombre de archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reporte_palinologico_{timestamp}.csv"
                
                # Exportar
                csv_data = df_export.to_csv(index=False)
                
                # Descargar archivo
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True
                )

# Footer
st.markdown("---")
st.markdown("*Sistema de Laboratorio Apícola - Reportes Palinológicos*") 