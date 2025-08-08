import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
from models.pool import Pool
from models.especie import Especie
from models.analisis_palinologico import AnalisisPalinologico
from components.contador_especies import ContadorEspecies
from components.pool_manager import PoolManager
from utils.calculators import validar_analisis, calcular_estadisticas_analisis
from utils.formatters import formatear_resumen_analisis, formatear_estadisticas, formatear_fecha_simple

# Configurar página
st.set_page_config(
    page_title="Análisis Palinológico - Laboratorio Apícola",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar manejo de errores
if 'error_count' not in st.session_state:
    st.session_state.error_count = 0

# Título de la página
st.title("🔬 Análisis Palinológico")
st.markdown("---")

# Inicializar modelos
pool_model = Pool()
especie_model = Especie()
analisis_model = AnalisisPalinologico()
contador_component = ContadorEspecies()
pool_manager = PoolManager()

# Sidebar para navegación
st.sidebar.title("🔬 Análisis Palinológico")
opcion = st.sidebar.radio(
    "Seleccione una opción:",
    ["Crear Nuevo Pool", "Realizar Análisis", "Ver Análisis Existentes"]
)

if opcion == "Crear Nuevo Pool":
    st.header("🆕 Crear Nuevo Pool")
    st.markdown("Cree un nuevo pool para realizar análisis palinológico.")
    
    # Crear pool
    pool_id = pool_manager.render_creacion_pool_completa()
    
    if pool_id:
        st.session_state['pool_creado_id'] = pool_id
        st.success(f"Pool #{pool_id} creado exitosamente. Ahora puede realizar el análisis.")

elif opcion == "Realizar Análisis":
    st.header("🔬 Realizar Análisis Palinológico")
    
    # Paso 1: Seleccionar pool
    st.subheader("📋 Paso 1: Seleccionar Pool")
    
    # Obtener pools disponibles con manejo de errores
    try:
        pools = pool_model.get_all_pools()
        
        if not pools:
            st.error("No hay pools disponibles. Por favor, cree un pool primero.")
            st.stop()
    except Exception as e:
        st.error(f"Error al cargar pools: {str(e)}")
        st.stop()
    
    # Crear opciones para el selector
    opciones_pools = []
    pools_dict = {}
    
    for pool in pools:
        # Obtener información del analista
        analista_nombre = "N/A"
        if pool.get('id_analista'):
            from models.analista import Analista
            analista_model = Analista()
            analista = analista_model.get_analista_by_id(pool['id_analista'])
            if analista:
                analista_nombre = f"{analista['nombres']} {analista['apellidos']}"
        
        opcion = f"Pool #{pool['id_pool']} - {analista_nombre} - {formatear_fecha_simple(pool['fecha_analisis'])}"
        opciones_pools.append(opcion)
        pools_dict[opcion] = pool['id_pool']
    
    # Selector de pool
    pool_seleccionado = st.selectbox(
        "Seleccione el pool para analizar:",
        options=opciones_pools,
        help="Seleccione el pool sobre el cual realizar el análisis"
    )
    
    if not pool_seleccionado:
        st.stop()
    
    pool_id = pools_dict[pool_seleccionado]
    
    # Mostrar información del pool seleccionado
    pool_info = pool_model.get_pool_with_details(pool_id)
    if pool_info:
        st.info(f"**Pool seleccionado:** #{pool_info['id_pool']} - Analista: {pool_info['analista_nombres']} {pool_info['analista_apellidos']} - Fecha: {formatear_fecha_simple(pool_info['fecha_analisis'])}")
    
    st.markdown("---")
    
    # Paso 2: Seleccionar especies
    st.subheader("🌿 Paso 2: Seleccionar Especies")
    
    # Obtener especies disponibles con manejo de errores
    try:
        especies = especie_model.get_all_especies()
        
        if not especies:
            st.error("No hay especies disponibles. Por favor, agregue especies primero.")
            st.stop()
    except Exception as e:
        st.error(f"Error al cargar especies: {str(e)}")
        st.stop()
    
    # Crear opciones para el multiselector
    opciones_especies = []
    especies_dict = {}
    
    for especie in especies:
        opcion = f"{especie['nombre_comun']} ({especie['nombre_cientifico']})"
        opciones_especies.append(opcion)
        especies_dict[opcion] = especie
    
    # Multiselector de especies
    especies_seleccionadas_opciones = st.multiselect(
        "Seleccione las especies a analizar:",
        options=opciones_especies,
        help="Puede seleccionar múltiples especies para el análisis"
    )
    
    # Obtener datos de especies seleccionadas
    especies_seleccionadas = [especies_dict[opcion] for opcion in especies_seleccionadas_opciones]
    
    if not especies_seleccionadas:
        st.info("Seleccione al menos una especie para continuar.")
        st.stop()
    
    st.markdown("---")
    
    # Paso 3: Contadores de especies
    st.subheader("🔢 Paso 3: Contar Granos de Polen")
    
    # Función callback para actualizar resumen
    def actualizar_resumen():
        pass  # Se ejecutará automáticamente
    
    # Renderizar contadores
    especies_data = contador_component.render_contadores_especies(
        especies_seleccionadas, 
        on_change=actualizar_resumen
    )
    
    # Mostrar resumen en tiempo real
    if especies_data:
        contador_component.mostrar_resumen_contadores(especies_data)
        
        # Validar datos
        validacion = contador_component.validar_contadores(especies_data)
        
        if not validacion['valido']:
            st.error("❌ Errores en el análisis:")
            for error in validacion['errores']:
                st.error(f"• {error}")
        
        if validacion['advertencias']:
            st.warning("⚠️ Advertencias:")
            for advertencia in validacion['advertencias']:
                st.warning(f"• {advertencia}")
        
        st.markdown("---")
        
        # Paso 4: Guardar análisis
        st.subheader("💾 Paso 4: Guardar Análisis")
        
        if validacion['valido']:
            if st.button("💾 Guardar Análisis", type="primary", use_container_width=True):
                with st.spinner("Guardando análisis..."):
                    # Filtrar solo especies con granos
                    especies_con_granos = [esp for esp in especies_data if esp.get('cantidad_granos', 0) > 0]
                    
                    if especies_con_granos:
                        # Guardar análisis
                        success = analisis_model.save_analisis_completo(pool_id, especies_con_granos)
                        
                        if success:
                            st.success("✅ Análisis guardado exitosamente!")
                            
                            # Mostrar resumen final
                            analisis_completo = analisis_model.get_analisis_completo(pool_id)
                            if analisis_completo:
                                st.markdown("### 📊 Resumen Final del Análisis")
                                st.markdown(formatear_resumen_analisis(analisis_completo))
                                
                                # Calcular y mostrar estadísticas
                                estadisticas = calcular_estadisticas_analisis(analisis_completo['analisis_especies'])
                                st.markdown(formatear_estadisticas(estadisticas))
                            else:
                                st.error("❌ No se pudo recuperar el análisis guardado")
                                st.info("Verifique la consola para más detalles de debug")
                            
                            # Limpiar contadores
                            contador_component.limpiar_contadores()
                            
                            # Limpiar selección de especies
                            if 'especies_seleccionadas' in st.session_state:
                                del st.session_state['especies_seleccionadas']
                            
                            st.rerun()
                        else:
                            st.error("❌ Error al guardar el análisis. Intente nuevamente.")
                    else:
                        st.error("❌ Debe contar al menos un grano de polen para guardar el análisis.")
        else:
            st.error("❌ Corrija los errores antes de guardar el análisis.")

elif opcion == "Ver Análisis Existentes":
    st.header("📋 Análisis Existentes")
    
    # Botón para verificar datos directamente en la BD
    if st.button("🔍 Verificar Datos en Base de Datos"):
        st.subheader("📊 Verificación Directa de Base de Datos")
        
        try:
            # Verificar pools
            pools = pool_model.get_all_pools()
            st.write(f"**Pools encontrados:** {len(pools)}")
            
            # Verificar análisis palinológicos
            from config.database import get_database_connection
            db = get_database_connection()
            
            # Consulta directa para análisis
            analisis_query = "SELECT COUNT(*) as total FROM analisis_palinologico"
            analisis_count = db.execute_query(analisis_query)
            st.write(f"**Análisis palinológicos en BD:** {analisis_count[0]['total'] if analisis_count else 0}")
            
            # Consulta directa para ver análisis por pool
            analisis_por_pool_query = """
                SELECT id_pool, COUNT(*) as total_analisis, SUM(cantidad_granos) as total_granos
                FROM analisis_palinologico 
                GROUP BY id_pool
                ORDER BY id_pool
            """
            analisis_por_pool = db.execute_query(analisis_por_pool_query)
            st.write("**Análisis por pool:**")
            for analisis in analisis_por_pool:
                st.write(f"- Pool {analisis['id_pool']}: {analisis['total_analisis']} análisis, {analisis['total_granos']} granos")
                
        except Exception as e:
            st.error(f"Error en verificación: {str(e)}")
    
    st.markdown("---")
    
    # Usar st.cache_data para evitar recargas innecesarias
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def cargar_analisis_existentes():
        try:
            analisis_completos = []
            pools = pool_model.get_all_pools()
            
            for pool in pools:
                try:
                    analisis = analisis_model.get_analisis_completo(pool['id_pool'])
                    if analisis:
                        analisis_completos.append(analisis)
                except Exception as e:
                    st.session_state.error_count += 1
                    if st.session_state.error_count <= 3:  # Limitar mensajes de error
                        st.warning(f"Error al cargar análisis del pool {pool['id_pool']}: {str(e)}")
                    continue
            
            return analisis_completos
        except Exception as e:
            st.error(f"Error al cargar análisis existentes: {str(e)}")
            return []
    
    # Cargar análisis con cache
    analisis_completos = cargar_analisis_existentes()
    
    # Debug: Mostrar información de pools disponibles
    try:
        pools = pool_model.get_all_pools()
        st.info(f"Pools disponibles en la base de datos: {len(pools)}")
        for pool in pools:
            st.write(f"- Pool #{pool['id_pool']} - Analista: {pool.get('id_analista', 'N/A')}")
    except Exception as e:
        st.warning(f"Error al obtener pools: {str(e)}")
    
    if not analisis_completos:
        st.info("No hay análisis realizados aún.")
        st.info("Esto puede deberse a:")
        st.info("1. No se han guardado análisis aún")
        st.info("2. Error en la recuperación de datos")
        st.info("3. Problemas de conexión con la base de datos")
    else:
        # Mostrar lista de análisis
        st.subheader("📊 Lista de Análisis Realizados")
        
        # Usar st.container para mejor rendimiento
        with st.container():
            for i, analisis in enumerate(analisis_completos):
                try:
                    pool_info = analisis.get('pool_info', {})
                    
                    # Crear título del expander de manera segura
                    titulo = f"Pool #{pool_info.get('id_pool', 'N/A')}"
                    if pool_info.get('analista_nombres') and pool_info.get('analista_apellidos'):
                        titulo += f" - {pool_info['analista_nombres']} {pool_info['analista_apellidos']}"
                    if pool_info.get('fecha_analisis'):
                        titulo += f" - {formatear_fecha_simple(pool_info['fecha_analisis'])}"
                    
                    with st.expander(titulo, expanded=False):
                        # Usar st.empty para evitar re-renders
                        resumen_container = st.empty()
                        resumen_container.markdown(formatear_resumen_analisis(analisis))
                        
                        # Mostrar tabla de especies
                        analisis_especies = analisis.get('analisis_especies', [])
                        if analisis_especies:
                            try:
                                import pandas as pd
                                from utils.formatters import crear_dataframe_analisis
                                
                                df_analisis = crear_dataframe_analisis(analisis_especies)
                                if not df_analisis.empty:
                                    st.dataframe(df_analisis, use_container_width=True, hide_index=True)
                                else:
                                    st.info("No hay datos de especies para mostrar en la tabla.")
                            except Exception as e:
                                st.warning(f"Error al crear tabla de especies: {str(e)}")
                        
                        # Mostrar estadísticas
                        try:
                            estadisticas = calcular_estadisticas_analisis(analisis_especies)
                            st.markdown(formatear_estadisticas(estadisticas))
                        except Exception as e:
                            st.warning(f"Error al calcular estadísticas: {str(e)}")
                
                except Exception as e:
                    st.error(f"Error al mostrar análisis {i+1}: {str(e)}")
                    continue

# Footer
st.markdown("---")
st.markdown("*Sistema de Laboratorio Apícola - Análisis Palinológico*") 