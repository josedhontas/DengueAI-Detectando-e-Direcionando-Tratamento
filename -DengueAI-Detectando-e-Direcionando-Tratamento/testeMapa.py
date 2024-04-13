import folium

def criar_mapa_ubs(dados_ubs):
    mapa = folium.Map(location=[-10.9092, -37.0628], zoom_start=8, tiles="openstreetmap")
    for dado in dados_ubs:
        folium.Marker([dado['Latitude'], dado['Longitude']], tooltip=dado['Nome']).add_to(mapa)
    return mapa

def criar_mapa_sintomas(data_dengue, centroids):
    mapa = folium.Map(location=[-10.9092, -37.0628], zoom_start=8, tiles="openstreetmap")
    for centroid in centroids:
        folium.Marker([centroid[0], centroid[1]], icon=folium.Icon(color='red'), tooltip='Centroide').add_to(mapa)
    return mapa

def criar_mapa_tempera_simulada(solucao_otimizada):
    mapa = folium.Map(location=[-10.9092, -37.0628], zoom_start=8, tiles="openstreetmap")
    for localizacao in solucao_otimizada:
        folium.Marker([localizacao['Latitude'], localizacao['Longitude']], tooltip='Solução Otimizada').add_to(mapa)
    return mapa
