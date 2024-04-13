import folium
from folium.plugins import HeatMap
from kmeans import KmeansClustering

def agrupar_clusters_sintomas(data):
    kmeans = KmeansClustering(k=5, iteration=200)
    y_kmeans = kmeans.fit(data[:, :2])
    clusters = [data[y_kmeans == i].tolist() for i in range(5)]
    return clusters

def criar_mapa_sintomas(clusters_sintomas):
    mapa = folium.Map(location=[-10.9092, -37.0628], zoom_start=8, tiles="openstreetmap")
    criar_mapa_clusters_sintomas(mapa, clusters_sintomas)
    return mapa

def criar_mapa_clusters_sintomas(mapa, clusters_sintomas):
    cores = ['blue', 'red', 'green', 'purple', 'orange']
    for i, cluster in enumerate(clusters_sintomas):
        for ponto in cluster:
            folium.CircleMarker(ponto[:2], radius=2, color=cores[i], fill_color=cores[i]).add_to(mapa)

def salvar_mapa_sintomas(mapa, nome_arquivo):
    mapa.save(nome_arquivo)
