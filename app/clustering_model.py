import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

class ClusteringModel:
    def __init__(self, vectorizer, kmeans):
        self.vectorizer = vectorizer
        self.kmeans = kmeans

    def predict_cluster(self, new_document):
        Y = self.vectorizer.transform([new_document])
        prediction = self.kmeans.predict(Y)
        return prediction

    def plot_clusters(self, tfidf_matrix, labels, method='pca', sample_size=5000, n_components=2):
        if len(labels) != tfidf_matrix.shape[0]:
            raise ValueError("Labels length must match the number of rows in the data matrix")

        indices = np.random.choice(tfidf_matrix.shape[0], size=min(sample_size, tfidf_matrix.shape[0]), replace=False)
        sampled_data = tfidf_matrix[indices]
        sampled_labels = np.array(labels)[indices]

        if method == 'pca':
            reducer = PCA(n_components=n_components)
        elif method == 'tsne':
            reducer = TSNE(n_components=n_components, perplexity=30, n_iter=1000)
        else:
            raise ValueError("Unsupported method")

        reduced_data = reducer.fit_transform(sampled_data.toarray())

        plt.figure(figsize=(10, 8))
        unique_labels = np.unique(sampled_labels)
        for label in unique_labels:
            label_indices = sampled_labels == label
            plt.scatter(reduced_data[label_indices, 0], reduced_data[label_indices, 1], alpha=0.8, label=f'Cluster {label}')

        plt.title(f'Clustering Visualization using {method.upper()}')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.legend()
        plt.show()
