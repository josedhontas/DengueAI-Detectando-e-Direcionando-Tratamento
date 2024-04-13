import csv
import math
import random

# Função para ler os dados da base de dados 1
def ler_base1(arquivo):
    with open(arquivo, 'r', newline='') as csvfile:
        leitor = csv.DictReader(csvfile, delimiter=';')
        dados = []
        for indice, linha in enumerate(leitor):
            if indice >= 30:
                break
            dados.append({
                'Latitude': float(linha['Latitude']),
                'Longitude': float(linha['Longitude']),
                'Dengue': int(linha['Dengue'])
            })
        return dados

# Função para ler os dados da base de dados 2
def ler_base2(arquivo):
    with open(arquivo, 'r', newline='') as csvfile:
        leitor = csv.DictReader(csvfile, delimiter=';')
        dados = []
        for indice, linha in enumerate(leitor):
            if indice >= 30:
                break
            dados.append({
                'Latitude': float(linha['latitude']),
                'Longitude': float(linha['longitude']),
                'Leitos': int(linha['leitos']),
                'Infectados': int(linha['qtd_infectados'])
            })
        return dados

# Função de custo
def funcao_custo(solucao, dados_base1, dados_base2):
    custo_total = 0
    for hospital in solucao:
        for pessoa in dados_base1:
            distancia = math.sqrt((hospital['Latitude'] - pessoa['Latitude']) ** 2 + (hospital['Longitude'] - pessoa['Longitude']) ** 2)
            custo_total += distancia * pessoa['Dengue']
        
        for unidade_saude in dados_base2:
            distancia = math.sqrt((hospital['Latitude'] - unidade_saude['Latitude']) ** 2 + (hospital['Longitude'] - unidade_saude['Longitude']) ** 2)
            custo_total += distancia * unidade_saude['Infectados']
    
    return custo_total

# Tempera simulada
def tempera_simulada(dominio, funcao_custo, temperatura=10000.0, resfriamento=0.95, passo=1, dados_base1=[], dados_base2=[]):
    solucao = [{'Latitude': random.uniform(dominio[0][0], dominio[0][1]), 'Longitude': random.uniform(dominio[1][0], dominio[1][1])} for _ in range(len(dados_base2))]

    while temperatura > 0.1:
        i = random.randint(0, len(solucao) - 1)
        direcao = random.randint(-passo, passo)

        solucao_temp = solucao[:]
        solucao_temp[i]['Latitude'] += direcao
        solucao_temp[i]['Longitude'] += direcao

        # Garante que as soluções estejam dentro do domínio
        solucao_temp[i]['Latitude'] = min(max(solucao_temp[i]['Latitude'], dominio[0][0]), dominio[0][1])
        solucao_temp[i]['Longitude'] = min(max(solucao_temp[i]['Longitude'], dominio[1][0]), dominio[1][1])

        custo_solucao = funcao_custo(solucao, dados_base1, dados_base2)
        custo_solucao_temp = funcao_custo(solucao_temp, dados_base1, dados_base2)
        probabilidade = math.exp((-custo_solucao_temp - custo_solucao) / temperatura)

        if custo_solucao_temp < custo_solucao or random.random() < probabilidade:
            solucao = solucao_temp

        temperatura *= resfriamento

    return solucao

# # Leitura dos dados
# dados_base1 = ler_base1('sintomas_dengue.csv')
# dados_base2 = ler_base2('ubs.csv')

# # Definição do domínio (limites para latitude e longitude)
# dominio = [(min(dados_base2, key=lambda x: x['Latitude'])['Latitude'], max(dados_base2, key=lambda x: x['Latitude'])['Latitude']),
#            (min(dados_base2, key=lambda x: x['Longitude'])['Longitude'], max(dados_base2, key=lambda x: x['Longitude'])['Longitude'])]

# # Aplicação da tempera simulada
# solucao_otimizada = tempera_simulada(dominio, funcao_custo, dados_base1=dados_base1, dados_base2=dados_base2)
# print("Solução otimizada:")
# print(solucao_otimizada)


# import folium

# mapa = folium.Map(location=[-10.6134055, -36.9541076], zoom_start=10)

# # Adicionando marcadores para cada coordenada otimizada
# for localizacao in solucao_otimizada:
#     lat = localizacao['Latitude']
#     long = localizacao['Longitude']
#     folium.Marker([lat, long], tooltip='Hospital ou Unidade de Saúde').add_to(mapa)

# # Exibindo o mapa
# mapa.save('mapa.html')  