import csv
import numpy as np
from DecisionTree import DecisionTree

class DenguePredictor:
    def __init__(self, data_file='E:/AtividadesUfs/IA-2022.2/-DengueAI-Detectando-e-Direcionando-Tratamento/-DengueAI-Detectando-e-Direcionando-Tratamento/sintomas_dengue.csv', test_size=0.2, random_state=42, max_depth=10):
        self.data_file = data_file
        self.test_size = test_size
        self.random_state = random_state
        self.max_depth = max_depth
        self.clf = None
        self.resultadoPredicao = None

    def load_data(self):
        data = []
        with open(self.data_file, mode='r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv, delimiter=';')
            for linha in leitor_csv:
                data.append(linha)

        X = np.array([x[1:-2] for x in data[1:]])  # Remova o último atributo (Dengue) e o penúltimo (Longitude)
        y = np.array([x[-1] for x in data[1:]]) 

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
        print("Acurácia do modelo de treinamento:", train_acc)

        test_predictions = self.clf.predict(self.X_test.astype(float))
        test_acc = self.accuracy(self.y_test.astype(int), test_predictions)
        print("Acurácia do modelo de teste:", test_acc)

    def make_prediction(self, novos_dados):
        sintomas = [novos_dados['febre'], novos_dados['dor_cabeca'], novos_dados['dor_articulacoes'],
                    novos_dados['sangramento'], novos_dados['latitude'], novos_dados['longitude'], novos_dados['idade']]
        self.resultadoPredicao  = self.clf.predict([sintomas])

        if self.resultadoPredicao [0] == 1:
            print(f"{novos_dados['nome']} tem dengue.")
        else:
            print(f"{novos_dados['nome']} não tem dengue.")

        sintomas_com_previsao = [novos_dados['nome']] + sintomas + [self.resultadoPredicao [0]]
        with open(self.data_file, mode='a', newline='') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv, delimiter=';')
            escritor_csv.writerow(sintomas_com_previsao)

        print(f'Informações de {novos_dados["nome"]} foram adicionadas à base de dados.')

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



