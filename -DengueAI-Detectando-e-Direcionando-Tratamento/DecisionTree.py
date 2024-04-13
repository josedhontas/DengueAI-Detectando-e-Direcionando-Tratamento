import numpy as np
from collections import Counter

class Node:
    def __init__(self, feature=None, limiar=None, left=None, right=None, *, valor=None):
        self.feature = feature
        self.limiar = limiar
        self.left = left
        self.right = right
        self.valor = valor
        
    def eh_no_folha(self):
        return self.valor is not None


class DecisionTree:
    def __init__(self, min_amostras_divisao=2, max_profundidade=100, n_caracteristicas=None):
        self.min_amostras_divisao = min_amostras_divisao
        self.max_profundidade = max_profundidade
        self.n_caracteristicas = n_caracteristicas
        self.raiz = None

    def fit(self, X, y):
        self.n_caracteristicas = X.shape[1] if not self.n_caracteristicas else min(X.shape[1],self.n_caracteristicas)
        self.raiz = self._crescer_arvore(X, y)

    def _crescer_arvore(self, X, y, profundidade=0):
        n_amostras, n_caracteristicas = X.shape
        n_labels = len(np.unique(y))

        # verifica os critérios de parada
        if (profundidade >= self.max_profundidade or n_labels == 1 or n_amostras < self.min_amostras_divisao):
            valor_folha = self._rotulo_mais_comum(y)
            return Node(valor=valor_folha)

        indices_caracteristicas = np.random.choice(n_caracteristicas, self.n_caracteristicas, replace=False)

        # encontrar a melhor divisão
        melhor_caracteristica, melhor_limiar = self._melhor_divisao(X, y, indices_caracteristicas)

        # criar nodos filhos
        indices_esquerda, indices_direita = self._dividir(X[:, melhor_caracteristica], melhor_limiar)
        left = self._crescer_arvore(X[indices_esquerda, :], y[indices_esquerda], profundidade + 1)
        right = self._crescer_arvore(X[indices_direita, :], y[indices_direita], profundidade + 1)
        return Node(melhor_caracteristica, melhor_limiar, left, right)


    def _melhor_divisao(self, X, y, indices_caracteristicas):
        melhor_ganho = -1
        indice_divisao, limiar_divisao = None, None

        for indice_caracteristica in indices_caracteristicas:
            coluna_X = X[:, indice_caracteristica]
            limiares = np.unique(coluna_X)

            for limiar in limiares:
                # calcular o ganho de informação
                ganho = self._ganho_informacao(y, coluna_X, limiar)

                if ganho > melhor_ganho:
                    melhor_ganho = ganho
                    indice_divisao = indice_caracteristica
                    limiar_divisao = limiar

        return indice_divisao, limiar_divisao


    def _ganho_informacao(self, y, coluna_X, limiar):
        # entropia do pai
        entropia_pai = self._entropia(y)

        # criar os filhos
        indices_esquerda, indices_direita = self._dividir(coluna_X, limiar)

        if len(indices_esquerda) == 0 or len(indices_direita) == 0:
            return 0
        
        # calcular a entropia média ponderada dos filhos
        n = len(y)
        n_esquerda, n_direita = len(indices_esquerda), len(indices_direita)
        entropia_esquerda, entropia_direita = self._entropia(y[indices_esquerda]), self._entropia(y[indices_direita])
        entropia_filhos = (n_esquerda/n) * entropia_esquerda + (n_direita/n) * entropia_direita

        # calcular o ganho de informação
        ganho_informacao = entropia_pai - entropia_filhos
        return ganho_informacao

    def _dividir(self, coluna_X, limiar_divisao):
        indices_esquerda = np.argwhere(coluna_X <= limiar_divisao).flatten()
        indices_direita = np.argwhere(coluna_X > limiar_divisao).flatten()
        return indices_esquerda, indices_direita

    def _entropia(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log(p) for p in ps if p > 0])


    def _rotulo_mais_comum(self, y):
        contador = Counter(y)
        valor = contador.most_common(1)[0][0]
        return valor

    def predict(self, X):
        return np.array([self._cortar_arvore(x, self.raiz) for x in X])

    def _cortar_arvore(self, x, node):
        if node.eh_no_folha():
            return node.valor

        if x[node.feature] <= node.limiar:
            return self._cortar_arvore(x, node.left)
        return self._cortar_arvore(x, node.right)