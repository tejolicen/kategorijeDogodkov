from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
import pandas as pd
import re
import os
import nltk
from nltk.stem import WordNetLemmatizer
import string
import lemmagen3
from lemmagen3 import Lemmatizer
import polyglot
from polyglot.text import Text, WordTokenizer
from polyglot.detect import Detector
#nltk.download()


set(stopwords.words('slovene'))





print_output = False


def preprocessText(item):
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

    lemmatizer = Lemmatizer('sl')
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
    preprocessedText = ' '.join(end_sentence)
    if(print_output):
        print('--------------------------------------------LENGTH > 2:')
        print(preprocessedText)
    return preprocessedText
