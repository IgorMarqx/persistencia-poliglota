import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
from datetime import datetime

# Importar módulos do projeto
from db_sqlite import SQLiteDB
from db_mongo import MongoDB
from geoprocessamento import GeoProcessamento

# Configuração da página
st.set_page_config(
    page_title="Sistema de Persistência Poliglota",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🗺️ Sistema de Persistência Poliglota")
st.markdown("**MongoDB + SQLite + Geoprocessamento**")
st.markdown("---")

# Inicializar conexões com bancos de dados
@st.cache_resource
def init_databases():
    """Inicializa as conexões com os bancos de dados"""
    sqlite_db = SQLiteDB()
    mongo_db = MongoDB()
    return sqlite_db, mongo_db

sqlite_db, mongo_db = init_databases()

# Sidebar para navegação
st.sidebar.title("📋 Menu")
pagina = st.sidebar.selectbox(
    "Escolha uma opção:",
    [
        "🏠 Início",
        "🏙️ Gerenciar Cidades (SQLite)",
        "📍 Gerenciar Locais (MongoDB)",
        "🔍 Consultas Integradas",
        "🌍 Geoprocessamento",
        "🗺️ Visualização no Mapa",
        "📊 Estatísticas"
    ]
)

# Página Inicial
if pagina == "🏠 Início":
    st.header("Bem-vindo ao Sistema de Persistência Poliglota!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 SQLite - Dados Estruturados")
        st.markdown("""
        - **Cidades e Estados** do Brasil
        - Dados tabulares estruturados
        - Relacionamentos entre tabelas
        - Consultas SQL tradicionais
        """)
        
        # Estatísticas do SQLite
        cidades = sqlite_db.get_cidades()
        estados = sqlite_db.get_estados()
        
        st.metric("Total de Cidades", len(cidades))
        st.metric("Total de Estados", len(estados))
    
    with col2:
        st.subheader("🗃️ MongoDB - Dados Geoespaciais")
        st.markdown("""
        - **Locais de interesse** com coordenadas
        - Documentos JSON flexíveis
        - Dados geográficos (lat/lng)
        - Consultas espaciais
        """)
        
        # Estatísticas do MongoDB
        locais = mongo_db.get_all_locais()
        st.metric("Total de Locais", len(locais))
        
        if locais:
            categorias = set(local.get('categoria', 'N/A') for local in locais)
            st.metric("Categorias", len(categorias))

# Página de Gerenciamento de Cidades (SQLite)
elif pagina == "🏙️ Gerenciar Cidades (SQLite)":
    st.header("🏙️ Gerenciamento de Cidades (SQLite)")
    
    tab1, tab2, tab3 = st.tabs(["📋 Listar Cidades", "➕ Adicionar Cidade", "📊 Dados de Exemplo"])
    
    with tab1:
        st.subheader("Lista de Cidades")
        cidades = sqlite_db.get_cidades()
        
        if cidades:
            df_cidades = pd.DataFrame(cidades)
            st.dataframe(df_cidades, use_container_width=True)
        else:
            st.info("Nenhuma cidade cadastrada. Use a aba 'Adicionar Cidade' ou 'Dados de Exemplo'.")
    
    with tab2:
        st.subheader("Adicionar Nova Cidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_cidade = st.text_input("Nome da Cidade")
            estado_uf = st.text_input("UF do Estado", max_chars=2, help="Ex: PB, PE, CE")
        
        with col2:
            populacao = st.number_input("População", min_value=0, value=0)
            area_km2 = st.number_input("Área (km²)", min_value=0.0, value=0.0)
        
        if st.button("Adicionar Cidade", type="primary"):
            if nome_cidade and estado_uf:
                try:
                    cidade_id = sqlite_db.insert_cidade(nome_cidade, estado_uf.upper(), 
                                                      populacao if populacao > 0 else None,
                                                      area_km2 if area_km2 > 0 else None)
                    st.success(f"Cidade '{nome_cidade}' adicionada com sucesso! ID: {cidade_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao adicionar cidade: {str(e)}")
            else:
                st.warning("Preencha pelo menos o nome da cidade e UF.")
    
    with tab3:
        st.subheader("Popular com Dados de Exemplo")
        st.markdown("Adiciona cidades e estados do Nordeste brasileiro.")
        
        if st.button("Popular Banco SQLite", type="secondary"):
            with st.spinner("Populando banco de dados..."):
                sqlite_db.populate_sample_data()
            st.success("Dados de exemplo adicionados com sucesso!")
            st.rerun()

# Página de Gerenciamento de Locais (MongoDB)
elif pagina == "📍 Gerenciar Locais (MongoDB)":
    st.header("📍 Gerenciamento de Locais (MongoDB)")
    
    tab1, tab2, tab3 = st.tabs(["📋 Listar Locais", "➕ Adicionar Local", "📊 Dados de Exemplo"])
    
    with tab1:
        st.subheader("Lista de Locais")
        locais = mongo_db.get_all_locais()
        
        if locais:
            # Converter para DataFrame
            df_locais = pd.DataFrame(locais)
            
            # Expandir coordenadas
            if 'coordenadas' in df_locais.columns:
                df_coords = pd.json_normalize(df_locais['coordenadas'])
                df_coords.columns = ['latitude', 'longitude']
                df_locais = pd.concat([df_locais.drop('coordenadas', axis=1), df_coords], axis=1)
            
            st.dataframe(df_locais, use_container_width=True)
        else:
            st.info("Nenhum local cadastrado. Use a aba 'Adicionar Local' ou 'Dados de Exemplo'.")
    
    with tab2:
        st.subheader("Adicionar Novo Local")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_local = st.text_input("Nome do Local")
            cidade = st.text_input("Cidade")
            categoria = st.selectbox("Categoria", ["Ponto Turístico", "Praça", "Comércio", "Cultura", "Praia", "Outros"])
            endereco = st.text_input("Endereço")
        
        with col2:
            latitude = st.number_input("Latitude", format="%.6f", value=-7.11532)
            longitude = st.number_input("Longitude", format="%.6f", value=-34.861)
            descricao = st.text_area("Descrição")
        
        if st.button("Adicionar Local", type="primary"):
            if nome_local and cidade and GeoProcessamento.validar_coordenadas(latitude, longitude):
                try:
                    local_id = mongo_db.insert_local(nome_local, cidade, latitude, longitude, 
                                                   descricao, categoria, endereco)
                    st.success(f"Local '{nome_local}' adicionado com sucesso! ID: {local_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao adicionar local: {str(e)}")
            else:
                st.warning("Preencha todos os campos obrigatórios e verifique as coordenadas.")
    
    with tab3:
        st.subheader("Popular com Dados de Exemplo")
        st.markdown("Adiciona locais de interesse do Nordeste brasileiro.")
        
        if st.button("Popular Banco MongoDB", type="secondary"):
            with st.spinner("Populando banco de dados..."):
                mongo_db.populate_sample_data()
            st.success("Dados de exemplo adicionados com sucesso!")
            st.rerun()

# Página de Consultas Integradas
elif pagina == "🔍 Consultas Integradas":
    st.header("🔍 Consultas Integradas")
    st.markdown("Cruza dados do SQLite (cidades) com MongoDB (locais)")
    
    # Selecionar cidade
    cidades = sqlite_db.get_cidades()
    if cidades:
        cidade_selecionada = st.selectbox(
            "Selecione uma cidade:",
            options=[f"{c['nome']} - {c['uf']}" for c in cidades],
            index=0
        )
        
        if cidade_selecionada:
            nome_cidade = cidade_selecionada.split(" - ")[0]
            
            # Buscar locais da cidade no MongoDB
            locais_cidade = mongo_db.get_locais_by_cidade(nome_cidade)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"📊 Informações da Cidade")
                cidade_info = next((c for c in cidades if c['nome'] == nome_cidade), None)
                if cidade_info:
                    st.json(cidade_info)
            
            with col2:
                st.subheader(f"📍 Locais em {nome_cidade}")
                if locais_cidade:
                    st.write(f"**{len(locais_cidade)} locais encontrados:**")
                    for local in locais_cidade:
                        with st.expander(f"📍 {local['nome_local']}"):
                            st.write(f"**Categoria:** {local.get('categoria', 'N/A')}")
                            st.write(f"**Descrição:** {local.get('descricao', 'N/A')}")
                            st.write(f"**Endereço:** {local.get('endereco', 'N/A')}")
                            coords = local.get('coordenadas', {})
                            st.write(f"**Coordenadas:** {coords.get('latitude', 'N/A')}, {coords.get('longitude', 'N/A')}")
                else:
                    st.info(f"Nenhum local encontrado para {nome_cidade}")
    else:
        st.warning("Nenhuma cidade cadastrada no SQLite.")

# Página de Geoprocessamento
elif pagina == "🌍 Geoprocessamento":
    st.header("🌍 Geoprocessamento")
    
    tab1, tab2 = st.tabs(["📍 Busca por Proximidade", "📏 Calcular Distância"])
    
    with tab1:
        st.subheader("Buscar Locais Próximos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            lat_central = st.number_input("Latitude Central", format="%.6f", value=-7.11532)
            lon_central = st.number_input("Longitude Central", format="%.6f", value=-34.861)
        
        with col2:
            raio_km = st.slider("Raio de Busca (km)", 1, 100, 10)
        
        if st.button("Buscar Locais Próximos", type="primary"):
            if GeoProcessamento.validar_coordenadas(lat_central, lon_central):
                # Buscar todos os locais
                todos_locais = mongo_db.get_all_locais()
                
                # Filtrar por proximidade
                locais_proximos = GeoProcessamento.locais_proximos(
                    todos_locais, lat_central, lon_central, raio_km
                )
                
                st.write(f"**{len(locais_proximos)} locais encontrados em um raio de {raio_km} km:**")
                
                if locais_proximos:
                    df_proximos = pd.DataFrame(locais_proximos)
                    
                    # Expandir coordenadas
                    if 'coordenadas' in df_proximos.columns:
                        df_coords = pd.json_normalize(df_proximos['coordenadas'])
                        df_coords.columns = ['latitude', 'longitude']
                        df_proximos = pd.concat([df_proximos.drop('coordenadas', axis=1), df_coords], axis=1)
                    
                    st.dataframe(df_proximos, use_container_width=True)
                else:
                    st.info("Nenhum local encontrado no raio especificado.")
            else:
                st.error("Coordenadas inválidas!")
    
    with tab2:
        st.subheader("Calcular Distância Entre Pontos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Ponto A:**")
            lat_a = st.number_input("Latitude A", format="%.6f", value=-7.11532, key="lat_a")
            lon_a = st.number_input("Longitude A", format="%.6f", value=-34.861, key="lon_a")
        
        with col2:
            st.write("**Ponto B:**")
            lat_b = st.number_input("Latitude B", format="%.6f", value=-8.04756, key="lat_b")
            lon_b = st.number_input("Longitude B", format="%.6f", value=-34.8770, key="lon_b")
        
        if st.button("Calcular Distância", type="primary"):
            if (GeoProcessamento.validar_coordenadas(lat_a, lon_a) and 
                GeoProcessamento.validar_coordenadas(lat_b, lon_b)):
                
                distancia = GeoProcessamento.calcular_distancia(lat_a, lon_a, lat_b, lon_b)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Distância", f"{distancia:.2f} km")
                with col2:
                    st.metric("Distância (Haversine)", f"{GeoProcessamento.distancia_haversine(lat_a, lon_a, lat_b, lon_b):.2f} km")
                with col3:
                    st.metric("Diferença", f"{abs(distancia - GeoProcessamento.distancia_haversine(lat_a, lon_a, lat_b, lon_b)):.4f} km")
            else:
                st.error("Coordenadas inválidas!")

# Página de Visualização no Mapa
elif pagina == "🗺️ Visualização no Mapa":
    st.header("🗺️ Visualização no Mapa")
    
    # Buscar todos os locais
    locais = mongo_db.get_all_locais()
    
    if locais:
        # Criar mapa centrado no Nordeste
        mapa = folium.Map(
            location=[-7.5, -37.0],  # Centro do Nordeste
            zoom_start=7,
            tiles='OpenStreetMap'
        )
        
        # Adicionar marcadores para cada local
        for local in locais:
            coords = local.get('coordenadas', {})
            if coords:
                lat = coords.get('latitude')
                lon = coords.get('longitude')
                
                if lat and lon:
                    # Criar popup com informações do local
                    popup_html = f"""
                    <div style="width: 200px;">
                        <h4>{local.get('nome_local', 'N/A')}</h4>
                        <p><strong>Cidade:</strong> {local.get('cidade', 'N/A')}</p>
                        <p><strong>Categoria:</strong> {local.get('categoria', 'N/A')}</p>
                        <p><strong>Descrição:</strong> {local.get('descricao', 'N/A')}</p>
                        <p><strong>Coordenadas:</strong> {lat:.6f}, {lon:.6f}</p>
                    </div>
                    """
                    
                    folium.Marker(
                        [lat, lon],
                        popup=folium.Popup(popup_html, max_width=300),
                        tooltip=local.get('nome_local', 'N/A'),
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(mapa)
        
        # Exibir mapa
        st_folium(mapa, width=700, height=500)
        
        # Estatísticas do mapa
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Locais", len(locais))
        with col2:
            cidades_unicas = len(set(local.get('cidade', '') for local in locais))
            st.metric("Cidades", cidades_unicas)
        with col3:
            categorias_unicas = len(set(local.get('categoria', '') for local in locais))
            st.metric("Categorias", categorias_unicas)
    
    else:
        st.info("Nenhum local cadastrado para visualizar no mapa.")

# Página de Estatísticas
elif pagina == "📊 Estatísticas":
    st.header("📊 Estatísticas do Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 SQLite - Cidades")
        cidades = sqlite_db.get_cidades()
        estados = sqlite_db.get_estados()
        
        if cidades:
            df_cidades = pd.DataFrame(cidades)
            
            # Estatísticas por estado
            stats_estado = df_cidades.groupby('uf').size().reset_index(name='quantidade')
            st.write("**Cidades por Estado:**")
            st.bar_chart(stats_estado.set_index('uf'))
            
            # População total
            pop_total = df_cidades['populacao'].sum()
            st.metric("População Total", f"{pop_total:,}")
    
    with col2:
        st.subheader("🗃️ MongoDB - Locais")
        locais = mongo_db.get_all_locais()
        
        if locais:
            df_locais = pd.DataFrame(locais)
            
            # Estatísticas por categoria
            if 'categoria' in df_locais.columns:
                stats_categoria = df_locais['categoria'].value_counts()
                st.write("**Locais por Categoria:**")
                st.bar_chart(stats_categoria)
            
            # Estatísticas por cidade
            if 'cidade' in df_locais.columns:
                stats_cidade = df_locais['cidade'].value_counts().head(10)
                st.write("**Top 10 Cidades:**")
                st.bar_chart(stats_cidade)
    
    # Estatísticas geográficas
    if locais:
        st.subheader("🌍 Estatísticas Geográficas")
        stats_geo = GeoProcessamento.estatisticas_geograficas(locais)
        
        if stats_geo:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total de Locais", stats_geo['total_locais'])
            with col2:
                st.metric("Latitude Média", f"{stats_geo['latitude_media']:.4f}")
            with col3:
                st.metric("Longitude Média", f"{stats_geo['longitude_media']:.4f}")
            with col4:
                centroide = stats_geo['centroide']
                st.metric("Centroide", f"{centroide[0]:.4f}, {centroide[1]:.4f}")

# Rodapé
st.markdown("---")
st.markdown("**Sistema de Persistência Poliglota** - Desenvolvido para o trabalho da faculdade")
st.markdown("**Tecnologias:** SQLite + MongoDB + Streamlit + Geopy + Folium")
