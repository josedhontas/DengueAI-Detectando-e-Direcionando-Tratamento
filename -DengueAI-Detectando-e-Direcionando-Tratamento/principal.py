import folium
from folium.plugins import HeatMap
from kmeans import KmeansClustering
from temperaSimulada import tempera_simulada, ler_base1, ler_base2, funcao_custo
import numpy as np
from folium.features import DivIcon
from opencage.geocoder import OpenCageGeocode  # Importação da biblioteca OpenCageGeocode

def ler_dados():
    dados_base1 = ler_base1('sintomas_dengue.csv')
    dados_base2 = ler_base2('ubs.csv')
    return dados_base1, dados_base2

def calcular_solucao_otimizada(dados_base1, dados_base2):
    dominio = [(min(dados_base2, key=lambda x: x['Latitude'])['Latitude'], max(dados_base2, key=lambda x: x['Latitude'])['Latitude']),
           (min(dados_base2, key=lambda x: x['Longitude'])['Longitude'], max(dados_base2, key=lambda x: x['Longitude'])['Longitude'])]
    solucao_otimizada = tempera_simulada(dominio, funcao_custo, dados_base1=dados_base1, dados_base2=dados_base2)
    # print("Solução otimizada:")
    # print(solucao_otimizada)
    return solucao_otimizada

def ler_dados_dengue_e_ubs():
    data_dengue = np.genfromtxt("sintomas_dengue.csv", delimiter=";", skip_header=1, usecols=(5, 6, 8))
    dados_ubs = np.genfromtxt("ubs.csv", delimiter=";", skip_header=1, usecols=(8, 9, 10, 11))
    return data_dengue, dados_ubs

def agrupar_clusters(data, k=5, iteration=200):
    kmeans = KmeansClustering(k=k, iteration=iteration)
    y_kmeans = kmeans.fit(data[:, :2])
    clusters = [data[y_kmeans == i].tolist() for i in range(k)]
    return clusters

def criar_mapa_clusters(mapa, clusters, cores):
    for i, cluster in enumerate(clusters):
        for ponto in cluster:
            folium.CircleMarker(ponto[:2], radius=2, color=cores[i], fill_color=cores[i]).add_to(mapa)

def adicionar_centroides(mapa, kmeans):
    centroids = kmeans.centroids
    for i, centroid in enumerate(centroids):
        folium.Marker(
            [centroid[0], centroid[1]],
            icon=DivIcon(
                icon_size=(10,10),
                icon_anchor=(5,5),
                html='<div style="font-size: 12pt; color: black;">X</div>'
            ),
            tooltip=f'Centroide do Cluster {i+1}'
        ).add_to(mapa)

def obter_endereco(lat, long, chave_api):
    geocoder = OpenCageGeocode(chave_api)
    resultado = geocoder.reverse_geocode(lat, long)
    if resultado:
        endereco = resultado[0]['formatted']
        return endereco
    else:
        return None

def adicionar_marcadores_otimizados(mapa, solucao_otimizada, chave_api):
    enderecos_adicionados = set()  # Conjunto para armazenar endereços já adicionados
    enderecos = []  # Vetor para armazenar os endereços

    for localizacao in solucao_otimizada:
        lat = localizacao['Latitude']
        long = localizacao['Longitude']
        endereco = obter_endereco(lat, long, chave_api)
        if endereco and endereco not in enderecos_adicionados:  # Verificar se o endereço não foi adicionado ainda
            enderecos.append(endereco)  # Adicionar o endereço ao vetor
            folium.Marker([lat, long], tooltip=f'Endereço: {endereco}').add_to(mapa)
            enderecos_adicionados.add(endereco)  # Adicionar o endereço ao conjunto de endereços adicionados
        elif not endereco:
            folium.Marker([lat, long], tooltip='Endereço não encontrado').add_to(mapa)
    
    return enderecos


def criar_mapa_calor(mapa, clusters):
    heat_data = [[point[0], point[1]] for cluster in clusters for point in cluster]
    HeatMap(heat_data, gradient={0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}).add_to(mapa)

def salvar_mapa(mapa, nome_arquivo):
    mapa.save(nome_arquivo)

def main():
    # Leitura dos dados
    dados_base1, dados_base2 = ler_dados()

    # Cálculo da solução otimizada
    solucao_otimizada = calcular_solucao_otimizada(dados_base1, dados_base2)

    # Leitura dos dados de sintomas de dengue e unidades de saúde
    data_dengue, dados_ubs = ler_dados_dengue_e_ubs()

    # Agrupamento dos clusters
    clusters_dengue = agrupar_clusters(data_dengue)
    clusters_ubs = agrupar_clusters(dados_ubs)

    # Criar o mapa
    mapa = folium.Map(location=[-10.9092, -37.0628], zoom_start=8, tiles="openstreetmap")

    # Adicionar marcadores dos clusters das unidades de saúde
    cores_ubs = ['blue', 'red', 'green', 'purple', 'orange']
    criar_mapa_clusters(mapa, clusters_ubs, cores_ubs)

    # Adicionar centróides dos clusters dos sintomas de dengue
    kmeans_dengue = KmeansClustering(k=5, iteration=200)
    y_kmeans_dengue = kmeans_dengue.fit(data_dengue[:, :2])
    adicionar_centroides(mapa, kmeans_dengue)


    # Adicionar marcadores otimizados
    chave_api = 'c098a7b3be6c4b4f9f14160c422559d5'  # Substitua pela sua chave de API do OpenCage Geocoding
    # adicionar_marcadores_otimizados(mapa, solucao_otimizada, chave_api)

    # Imprimir os centroides na tela
    centroids = kmeans_dengue.centroids
    print("Coordenadas dos centroides:")
    for i, centroid in enumerate(centroids):
        # print(f"Centroide {i+1}: Latitude {centroid[0]}, Longitude {centroid[1]}")
        end_cluster = obter_endereco(centroid[0], centroid[1], chave_api)
        print(end_cluster)



    enderecos = adicionar_marcadores_otimizados(mapa, solucao_otimizada, chave_api)

    # Imprimir os endereços na função principal
    for endereco in enderecos:
        print(endereco)

    # Criar mapa de calor
    criar_mapa_calor(mapa, clusters_dengue)

    # Salvar o mapa como HTML
    salvar_mapa(mapa, "mapa.html")
    
    

if __name__ == "__main__":
    main()
