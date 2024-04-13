import csv
import numpy as np
from DecisionTree import DecisionTree

class MinMaxScalerCustom:
    def __init__(self):
        self.min = None
        self.max = None

    def fit(self, X):
        self.min = np.min(X, axis=0)
        self.max = np.max(X, axis=0)

    def transform(self, X):
        return (X - self.min) / (self.max - self.min)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

class DenguePredictor:
    def __init__(self, data_file='./dataBase/sintomas_dengue.csv', test_size=0.2, random_state=42, max_depth=10):
        self.data_file = data_file
        self.test_size = test_size
        self.random_state = random_state
        self.max_depth = max_depth
        self.clf = None
        self.resultadoPredicao = None
        self.scaler = MinMaxScalerCustom()

    def load_data(self):
        data = []
        with open(self.data_file, mode='r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv, delimiter=';')
            for linha in leitor_csv:
                data.append(linha)

        X = np.array([x[1:-2] for x in data[1:]])  # Remova o último atributo (Dengue) e o penúltimo (Longitude)
        y = np.array([x[-1] for x in data[1:]]) 

        # Normalizar latitude e longitude
        lat_long = np.array([[float(x[-2]), float(x[-1])] for x in data[1:]])
        lat_long_normalized = self.scaler.fit_transform(lat_long)

        X[:, 4:6] = lat_long  # Armazenar as coordenadas originais

        self.X_train, self.X_test, self.y_train, self.y_test = self.train_test_split_custom(X, y, test_size=self.test_size, random_state=self.random_state)

    def train_test_split_custom(self, X, y, test_size=0.2, random_state=None):
        np.random.seed(random_state)
        indices = np.random.permutation(len(X))
        test_size = int(test_size * len(X))
        test_indices = indices[:test_size]
        train_indices = indices[test_size:]

        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]

        return X_train, X_test, y_train, y_test

    def train_model(self):
        self.clf = DecisionTree(max_profundidade=self.max_depth)
        self.clf.fit(self.X_train.astype(float), self.y_train.astype(int))

    def evaluate_model(self):
        train_predictions = self.clf.predict(self.X_train.astype(float))
        train_acc = self.accuracy(self.y_train.astype(int), train_predictions)
        # print("Acurácia do modelo de treinamento:", train_acc)

        test_predictions = self.clf.predict(self.X_test.astype(float))
        test_acc = self.accuracy(self.y_test.astype(int), test_predictions)
        # print("Acurácia do modelo de teste:", test_acc)

    def make_prediction(self, novos_dados):
        sintomas = [novos_dados['febre'], novos_dados['dor_cabeca'], novos_dados['dor_articulacoes'],
                    novos_dados['sangramento'], novos_dados['latitude'], novos_dados['longitude'], novos_dados['idade']]

        # Normalizar latitude e longitude dos novos dados
        lat_long_normalized = self.scaler.transform([[novos_dados['latitude'], novos_dados['longitude']]])
        sintomas[4:6] = [novos_dados['latitude'], novos_dados['longitude']]  # Armazenar as coordenadas originais

        self.resultadoPredicao = self.clf.predict([sintomas])

        # if self.resultadoPredicao[0] == 1:
            # print(f"{novos_dados['nome']} tem dengue.")
        # else:
            # print(f"{novos_dados['nome']} não tem dengue.")

        sintomas_com_previsao = [novos_dados['nome']] + sintomas + [self.resultadoPredicao[0]]
        with open(self.data_file, mode='a', newline='') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv, delimiter=';')
            escritor_csv.writerow(sintomas_com_previsao)

        # print(f'Informações de {novos_dados["nome"]} foram adicionadas à base de dados.')

    @staticmethod
    def accuracy(y_true, y_pred):
        return np.sum(y_true == y_pred) / len(y_true)

def dataAcess(novos_dados):
    predictor = DenguePredictor()
    predictor.load_data()
    predictor.train_model()
    predictor.evaluate_model()

    predictor.make_prediction(novos_dados)

    # Obtendo a previsão feita pela função make_prediction
    resultado_predicao = predictor.resultadoPredicao

    # Convertendo a previsão para um tipo serializável (int)
    exame_serializavel = int(resultado_predicao[0])

    resultado_post = {
        "nome": novos_dados["nome"],
        "latitude": novos_dados["latitude"],
        "longitude": novos_dados["longitude"],
        "idade": novos_dados["idade"],
        "exame": exame_serializavel
    }

    return resultado_post

# # Exemplo 1
# novos_dados1 = {
#     "nome": "João",
#     "febre": 1,
#     "dor_cabeca": 1,
#     "dor_articulacoes": 1,
#     "sangramento": 0,
#     "latitude": 37.7749,
#     "longitude": -122.4194,
#     "idade": 25
# }
# resultado_previsao1 = dataAcess(novos_dados1)
# print(resultado_previsao1)

# # Exemplo 2
# novos_dados2 = {
#     "nome": "Maria",
#     "febre": 0,
#     "dor_cabeca": 1,
#     "dor_articulacoes": 0,
#     "sangramento": 1,
#     "latitude": 34.0522,
#     "longitude": -118.2437,
#     "idade": 40
# }
# resultado_previsao2 = dataAcess(novos_dados2)
# print(resultado_previsao2)

# # Exemplo 3
# novos_dados3 = {
#     "nome": "Pedro",
#     "febre": 1,
#     "dor_cabeca": 1,
#     "dor_articulacoes": 1,
#     "sangramento": 1,
#     "latitude": 41.8781,
#     "longitude": -87.6298,
#     "idade": 35
# }
# resultado_previsao3 = dataAcess(novos_dados3)
# print(resultado_previsao3)

# # Exemplo 4
# novos_dados4 = {
#     "nome": "Ana",
#     "febre": 0,
#     "dor_cabeca": 0,
#     "dor_articulacoes": 0,
#     "sangramento": 0,
#     "latitude": 51.5074,
#     "longitude": -0.1278,
#     "idade": 50
# }
# resultado_previsao4 = dataAcess(novos_dados4)
# print(resultado_previsao4)

# # Exemplo 5
# novos_dados5 = {
#     "nome": "Luiz",
#     "febre": 1,
#     "dor_cabeca": 0,
#     "dor_articulacoes": 0,
#     "sangramento": 1,
#     "latitude": 35.6895,
#     "longitude": 139.6917,
#     "idade": 45
# }
# resultado_previsao5 = dataAcess(novos_dados5)
# print(resultado_previsao5)

# Exemplo 6
# novos_dados6 = {
#     "nome": "Carla",
#     "febre": 0,
#     "dor_cabeca": 1,
#     "dor_articulacoes": 1,
#     "sangramento": 0,
#     "latitude": -33.8688,
#     "longitude": 151.2093,
#     "idade": 30
# }
# resultado_previsao6 = dataAcess(novos_dados6)
# print(resultado_previsao6)
