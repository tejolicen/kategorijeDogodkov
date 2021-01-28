
from sklearn import svm
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
from collections import Counter


__file__ = os.getcwd()
dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'scripts\\data\\dogodki50_spucano_glavnekategorije.csv')
df = pd.read_csv(input_file, header = 0)

dfVeselice = df.loc[df['veselica'] == 1]
dfNeznane = df.loc[df['veselica'] == 0]

print('veselice count: ' + str(len(dfVeselice)) + ', neznane count: ' + str(len(dfNeznane)))

vectorizer = TfidfVectorizer()

train_vectors = vectorizer.fit_transform(dfVeselice.opis)
test_vectors = vectorizer.transform(dfNeznane.opis)

model = svm.OneClassSVM(gamma='auto')
model.fit(train_vectors)

test_predictions = model.predict(test_vectors)

print(Counter(test_predictions))


#### ------------------- #####


# train = fetch_20newsgroups(subset='train', categories=['alt.atheism'], shuffle=True, random_state=42).data
# test =  fetch_20newsgroups(subset='train', categories=['alt.atheism', 'soc.religion.christian'], shuffle=True, random_state=42).data

# vectorizer = TfidfVectorizer()
# train_vectors = vectorizer.fit_transform(train)
# test_vectors = vectorizer.transform(test)

# model = svm.OneClassSVM(gamma='auto')
# model.fit(train_vectors)

# test_predictions = model.predict(test_vectors)

# print(test_predictions)