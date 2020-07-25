from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn import metrics
import numpy as np
import pandas as pd
import os
from sklearn.decomposition import PCA





dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'data/la.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis = df['opis']
data_types = df['event_type']
data_typesFirst = []
allTypes = []
dataLength = len(data_types)


for i in range(dataLength):
    types_split = data_types[i].split(', ')
    for j in range(len(types_split)):
        if types_split[j] not in allTypes:
            allTypes.append(types_split[j])
    data_typesFirst.append(types_split[0])

print(allTypes)


labels = []

for i in range(len(data_typesFirst)):
    labels.append(allTypes.index(data_typesFirst[i]))

print(allTypes)
print('dataCount: ' + str(len(data_opis)) + ', labelCount: ' + str(len(labels)))


true_k = 5


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