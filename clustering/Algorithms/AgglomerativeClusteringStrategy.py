from sklearn.cluster import AgglomerativeClustering
from clustering.ClusteringStrategy import ClusteringStrategy


class AgglomerativeClusteringStrategy(ClusteringStrategy):
    def cluster(self, distance_matrix, n_clusters):
        """Clusters data points using Agglomerative Clustering."""
        model = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage='average')
        cluster_labels = model.fit_predict(distance_matrix)
        return cluster_labels
