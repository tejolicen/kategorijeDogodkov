import os
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn import decomposition, cluster

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import polyglot
import math
from polyglot.text import Text, Word


__file__ = os.getcwd()
dirname = __file__ #os.path.dirname(__file__)
input_file = os.path.join(dirname, 'scripts\\data\\dogodki100_strippedOnlySlov.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis_normalized = df['opis'].astype('U')



def get_top_keywords(data, clusters, labels, n_terms):
    df = pd.DataFrame(data).groupby(clusters).mean()
    
    for i,r in df.iterrows():
        print('Cluster {}: '.format(i) + ', '.join([labels[t] for t in np.argsort(r)[-n_terms:]]))


no_features = 2000
vectorizer = TfidfVectorizer(use_idf=True, max_df=0.95, min_df=2, max_features=no_features)  #stop_words='english', 
X_idf = vectorizer.fit_transform(data_opis_normalized)


# agglo = cluster.FeatureAgglomeration(n_clusters=100)
# agglo.fit(X_idf.todense())
# X_reduced = agglo.transform(X_idf.todense())
# X_reduced = X_idf.todense()


# We train the PCA on the dense version of the tf-idf. 
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_idf.todense())


tsne = TSNE(n_components=2, verbose=1, perplexity=30, n_iter=5000, learning_rate=200)
X_tsne = tsne.fit_transform(X_idf.todense())

n_clusters = 7

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# Initialize the clusterer with n_clusters value
clusterer_pca = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1, random_state=1) # random_state = 1 (seed)
cluster_labels_pca = clusterer_pca.fit_predict(X_pca)
centers_pca = clusterer_pca.cluster_centers_
centerDistances_pca = []
for i in range(len(cluster_labels_pca)):
    centerDistances_pca.append(distance(centers_pca[cluster_labels_pca[i]], X_pca[i]))  # distanca med centrom gruče in dogodkom


# Initialize the clusterer with n_clusters value
clusterer_tsne = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1, random_state=1) # random_state = 1 (seed)
cluster_labels_tsne = clusterer_tsne.fit_predict(X_tsne)
centers_tsne = clusterer_tsne.cluster_centers_
centerDistances_tsne = []
for i in range(len(cluster_labels_tsne)):
    centerDistances_tsne.append(distance(centers_tsne[cluster_labels_tsne[i]], X_tsne[i]))  # distanca med centrom gruče in dogodkom



df['cluster_pca'] = cluster_labels_pca
df['center_distance_pca'] = centerDistances_pca

df['cluster_tsne'] = cluster_labels_tsne
df['center_distance_tsne'] = centerDistances_tsne

df.to_csv(os.path.join(dirname, 'scripts\\data\\dogodki100_kmeansResults.csv'), index = False)

for i in range(n_clusters):
    loc_cluster_pca_DF = df.loc[df['cluster_pca'] == i]
    loc_cluster_pca_DF_sorted = loc_cluster_pca_DF.sort_values(by=['cluster_pca', 'center_distance_pca'])
    loc_cluster_pca_DF_sorted[:20].to_csv(os.path.join(dirname, 'scripts\\data\\kmeans_clusters\\cluster_pca_' + str(i) + '_top20_.csv'), index = False)
    loc_cluster_tsne_DF = df.loc[df['cluster_tsne'] == i]
    loc_cluster_tsne_DF_sorted = loc_cluster_tsne_DF.sort_values(by=['cluster_tsne', 'center_distance_tsne'])
    loc_cluster_tsne_DF_sorted[:20].to_csv(os.path.join(dirname, 'scripts\\data\\kmeans_clusters\\cluster_tsne_' + str(i) + '_top20_.csv'), index = False)



# The silhouette_score gives the average value for all the samples.
# This gives a perspective into the density and separation of the formed
# clusters
silhouette_avg = silhouette_score(X, cluster_labels)
print()
print()
print("For n_clusters =", n_clusters,
        "The average silhouette_score is :", silhouette_avg)
    
print()

get_top_keywords(X_idf.todense(), cluster_labels, vectorizer.get_feature_names(), 10)
# Compute the silhouette scores for each sample
sample_silhouette_values = silhouette_samples(X, cluster_labels)

y_lower = 10
for i in range(n_clusters):
    # Aggregate the silhouette scores for samples belonging to
    # cluster i, and sort them
    ith_cluster_silhouette_values = \
        sample_silhouette_values[cluster_labels == i]

    ith_cluster_silhouette_values.sort()

    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = cm.nipy_spectral(float(i) / n_clusters)
    ax1.fill_betweenx(np.arange(y_lower, y_upper),
                        0, ith_cluster_silhouette_values,
                        facecolor=color, edgecolor=color, alpha=0.7)

    # Label the silhouette plots with their cluster numbers at the middle
    ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

    # Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

ax1.set_title("The silhouette plot for the various clusters.")
ax1.set_xlabel("The silhouette coefficient values")
ax1.set_ylabel("Cluster label")

# The vertical line for average silhouette score of all the values
ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

ax1.set_yticks([])  # Clear the yaxis labels / ticks
ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

# 2nd Plot showing the actual clusters formed
colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
            c=colors, edgecolor='k')

# Labeling the clusters
centers = clusterer.cluster_centers_
# Draw white circles at cluster centers
ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
            c="white", alpha=1, s=200, edgecolor='k')

for i, c in enumerate(centers):
    ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                s=50, edgecolor='k')

ax2.set_title("The visualization of the clustered data.")
ax2.set_xlabel("Feature space for the 1st feature")
ax2.set_ylabel("Feature space for the 2nd feature")

plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                "with n_clusters = %d" % n_clusters),
                fontsize=14, fontweight='bold')
          

plt.show()