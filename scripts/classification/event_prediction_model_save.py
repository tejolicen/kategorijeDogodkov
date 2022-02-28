from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
import sys
from sklearn import metrics

from nltk.classify.scikitlearn import SklearnClassifier
import pickle


__file__ = os.getcwd()
dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'scripts\\data\\dogodki50_spucano_glavnekategorije_veselice.csv')
df = pd.read_csv(input_file, header = 0)

df['category_id'] = df['kategorije_nazivi_new'].factorize()[0]
category_id_df = df[['kategorije_nazivi_new', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'kategorije_nazivi_new']].values)

df.sample(n=400, replace=True, random_state=1) # sample v primeru _PROBA

tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.95, min_df=4, ngram_range=(1, 2), norm='l2')

features = tfidf.fit_transform(df.opispp).toarray()
labels = df.category_id

#model = LinearSVC()
model = SVC(kernel='linear',probability=True)

X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.2, random_state=0)
model.fit(X_train, y_train)
#y_pred = model.predict(X_test)
y_pred = model.predict_proba(X_test)

# save the model to disk
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'scripts/data/_model.pickle')
pickle.dump(model, open(filename, 'wb'))
filenameTFIDF = os.path.join(dirname, 'scripts/data/_tfidf.pickle')
pickle.dump(tfidf, open(filenameTFIDF, 'wb'))

conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.kategorije_nazivi_new.values, yticklabels=category_id_df.kategorije_nazivi_new.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()
print(metrics.classification_report(y_test, y_pred, 
                                    target_names=df['kategorije_nazivi_new'].unique()))




