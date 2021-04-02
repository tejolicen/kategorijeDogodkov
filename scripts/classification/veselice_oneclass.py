
from sklearn import svm
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
from collections import Counter
import msvcrt  

__file__ = os.getcwd()
dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'scripts\\data\\dogodki50_spucano_glavnekategorije.csv')
df = pd.read_csv(input_file, header = 0)

dfVeselice = df.loc[df['veselica'] == 1]
dfNeznane = df.loc[df['veselica'] == 0]

print('veselice count: ' + str(len(dfVeselice)) + ', neznane count: ' + str(len(dfNeznane)))

vectorizer = TfidfVectorizer()

train_vectors = vectorizer.fit_transform(dfVeselice.opispp)
test_vectors = vectorizer.transform(df.opispp)

model = svm.OneClassSVM(gamma='auto', kernel='rbf')
model.fit(train_vectors)

test_predictions = model.predict(test_vectors)

test_prediction_score = model.score_samples(test_vectors)
print(Counter(test_predictions))
print(test_prediction_score)

df['is_veselica_prediction'] = test_predictions
df['is_veselica_prediction_score'] = test_prediction_score
df.sort_values(by=['is_veselica_prediction_score'], inplace=True, ascending=False)
arrVeseliceNove = []

#for index, row in df.iterrows():
#    print(str(row['is_veselica_prediction']) + ', score: ' + str(row['is_veselica_prediction_score']))

for index, row in df.iterrows():
    if(row['is_veselica_prediction'] == 0 and row['veselica'] == 1):
        print('Čudna napoved!')
    if(row['is_veselica_prediction'] == 1 and row['veselica'] == 0):
        print('\n')
        print(row['naziv'] + ' | ' +row['kategorije_nazivi_new']+'\n'+ row['opis'])
        print('Je veselica? (Y/N)')
        inp = msvcrt.getche().decode('ASCII') 

        if(inp.lower() == 'y'):
            row['veselica'] = 1
    arrVeseliceNove.append(row['veselica'])


    

df['veselicaNew'] = arrVeseliceNove


for index, row in df.iterrows():
    if(row['veselicaNew'] == 1):
        df.loc[index, 'kategorije_nazivi_new'] = 'Veselica'
        df.loc[index, 'kategorije_sifre_new'] = 999

output_file = os.path.join(dirname, 'scripts\\data\\dogodki50_spucano_glavnekategorije1.csv')
df.to_csv(output_file, index = False)

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