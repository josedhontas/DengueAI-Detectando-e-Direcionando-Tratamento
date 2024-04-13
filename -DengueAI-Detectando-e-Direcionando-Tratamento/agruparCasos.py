import numpy as np
import folium
from folium.plugins import HeatMap
from kmeans import KmeansClustering

# Leitura dos dados
data = np.genfromtxt("sintomas_dengue.csv", delimiter=";", skip_header=1, usecols=(5, 6, 8))

# Filtrar apenas os dados com Dengue = 1
data_dengue = data[data[:, 2] == 1]

# Usar KmeansClustering
kmeans = KmeansClustering(k=5, iteration=200)
y_kmeans = kmeans.fit(data_dengue[:, :2])  # Apenas latitude e longitude são usadas para o clustering

# Criar listas de coordenadas para cada cluster
clusters = []
for i in range(5):
    cluster = data_dengue[y_kmeans == i].tolist()
    clusters.append(cluster)

# Calcular os centroides de cada cluster
centroids = [np.mean(cluster, axis=0)[:2] for cluster in clusters]

# Criar o mapa
map = folium.Map(location=[-10.9092, -37.0628], zoom_start=12, tiles="openstreetmap")  # Definir localização inicial com base nas coordenadas médias

# Adicionar marcadores de círculo para cada cluster no mapa
colors = ['blue', 'red', 'green', 'purple', 'orange']
for i, cluster in enumerate(clusters):
    for point in cluster:
        folium.CircleMarker(point[:2], radius=2, color=colors[i], fill_color=colors[i]).add_to(map)

# Adicionar marcadores para os centroides
for centroid in centroids:
    folium.Marker(centroid, icon=folium.Icon(color='black')).add_to(map)

# Calcular a densidade de pontos e criar o mapa de calor
heat_data = [[point[0], point[1]] for cluster in clusters for point in cluster]
HeatMap(heat_data, gradient={0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}).add_to(map)

# Salvar o mapa como HTML
map.save("mapa_clusters_dengue.html")

