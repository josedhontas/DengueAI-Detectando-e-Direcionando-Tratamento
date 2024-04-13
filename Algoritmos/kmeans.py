import numpy as np
import matplotlib.pyplot as plt
'''
- OS dados são definidos aleatoriamente dentro do conjunto de dados disponíveis no dataset
- Calcular a distância entre cada data point distância Euclidiana

'''

class KmeansClustering:
    def __init__(self, k=3, iteration=200):
        self.k = k
        self.iteration = iteration
        self.centroids = None

    def init_centroids(self, X):
        self.centroids = np.random.uniform(np.amin(X, axis=0), np.amax(X, axis=0), size=(self.k, X.shape[1]))

    @staticmethod
    def euclidian_distance(data_point, centroids):
        return np.sqrt(np.sum((centroids - data_point)**2, axis=1))

    def fit(self, X):
        self.init_centroids(X)
        y = []  # Inicialização de y
        for _ in range(self.iteration):
            y.clear()  # Limpar y antes de cada iteração
            for data_point in X:
                distances = KmeansClustering.euclidian_distance(data_point, self.centroids)
                cluster_num = np.argmin(distances)
                y.append(cluster_num)

            cluster_indices = []
            for i in range(self.k):
                cluster_indices.append(np.argwhere(np.array(y) == i))

            cluster_centers = []
            for indices in cluster_indices:
                if len(indices) == 0:
                    cluster_centers.append(self.centroids[i])
                else:
                    cluster_centers.append(np.mean(X[indices], axis=0)[0])
            if np.max(self.centroids - np.array(cluster_centers)) < 0.0001:
                break
            else:
                self.centroids = np.array(cluster_centers)
        return np.array(y)
    
    

# random_points = np.random.randint(0, 100, (100,2))
# print (random_points)
# kmeans = KmeansClustering(k=3, iteration=200)
# labels = kmeans.fit(random_points)

# plt.scatter(random_points[:,0], random_points[:,1], c = labels)
# plt.scatter(kmeans.centroids[:,0], kmeans.centroids[:,1], c=range(len(kmeans.centroids)), marker="*", s=200)
# plt.show()

        
        


    

