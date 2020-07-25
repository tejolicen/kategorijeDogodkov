from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
import pandas as pd
import re
import os
import nltk
from nltk.stem import WordNetLemmatizer
import string
import lemmagen.lemmatizer
from lemmagen.lemmatizer import Lemmatizer
#nltk.download()

set(stopwords.words('slovene'))




dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'data/dogodki.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis = df['opis'].astype('U')
dataLength = len(data_opis)

print_output = False

def normalize(arr):
    normalizedArr = []
    for item in arr:
        if(print_output):
            print('--------------------------------------------INPUT ITEM:')
            print(item)

        no_links = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', "", item)
        
        if(print_output):
            print('--------------------------------------------REMOVE URLS:')
            print(no_links)
        
        word_tokens = word_tokenize(no_links) 

        word_tokens = [w.lower() for w in word_tokens]
        
        if(print_output):
            print('--------------------------------------------TO LOWER:')
            print(' '.join(word_tokens))

        table = str.maketrans('', '', string.punctuation)
        word_tokens = [w.translate(table) for w in word_tokens]
        # remove remaining tokens that are not alphabetic
        word_tokens = [word for word in word_tokens if word.isalpha()]

        if(print_output):
            print('--------------------------------------------ONLY ALPHABETIC:')
            print(' '.join(word_tokens))

        stop_words = set(stopwords.words('slovene')) 
        filtered_sentence = [] 
        for w in word_tokens: 
            if w not in stop_words and len(w) > 1: 
                filtered_sentence.append(w) 

        if(print_output):
            print('--------------------------------------------REMOVE STOPWORDS:')
            print(' '.join(filtered_sentence))

        #Stem_words = []
        #ps =PorterStemmer()
        #for w in filtered_sentence:
        #    rootWord=ps.stem(w)
        #    Stem_words.append(rootWord)

        #if(print_output):
        #    print('--------------------------------------------STEMMING:')
        #    print(' '.join(Stem_words))

        lemmatizer = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)
        lemma_word = []
        #wordnet_lemmatizer = WordNetLemmatizer()
        for w in filtered_sentence:
            word1 = lemmatizer.lemmatize(w)
            #word2 = wordnet_lemmatizer.lemmatize(word1, pos = "v")
            #word3 = wordnet_lemmatizer.lemmatize(word2, pos = ("a"))
            lemma_word.append(word1)

        if(print_output):
            print('--------------------------------------------LEMMATIZATION(LemmaGen):')
            print(' '.join(lemma_word))

        end_sentence = []

        for w in lemma_word: 
            if len(w) > 2: 
                end_sentence.append(w) 

        if(print_output):
            print('--------------------------------------------LENGTH > 2:')
            print(' '.join(end_sentence))
        normalizedArr.append(' '.join(end_sentence))

    return normalizedArr



### Da nazaj shraniš podatk2 ###
data_normalized = normalize(data_opis)
df['opis'] = data_normalized
df.to_csv(os.path.join(dirname, 'data/dogodki_stripped1.csv'), index = False)
