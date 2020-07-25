
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import polyglot
import os
from polyglot.text import Text, Word
from polyglot.mapping import Embedding

import nltk
from nltk.corpus import stopwords





dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'data/dogodki.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis = df['opis'].astype('U')
dataLength = len(data_opis)

row = data_opis[1]

text = Text(row)
word = Word(row)

stopwords = stopwords.words('slovene')

print(stopwords)
print(row)
print('-------------------------------------------------')
print(text.words)
print(text.pos_tags)
print('-------------------------------------------------')
#print(text.entities)
#print(text.morphemes)


#for i in range(dataLength):
    

