from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn import metrics
import numpy as np
import pandas as pd
import os


dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'data/dogodki.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis = df['opis'].astype('U')




labels = []



true_k = 12


vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data_opis)

model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, model.labels_))
print("Completeness: %0.3f" % metrics.completeness_score(labels, model.labels_))
print("V-measure: %0.3f" % metrics.v_measure_score(labels, model.labels_))
print("Adjusted Rand-Index: %.3f"
      % metrics.adjusted_rand_score(labels, model.labels_))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, model.labels_, sample_size=1000))

print()

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d: " % (i))
    print("\t\t\t", end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()