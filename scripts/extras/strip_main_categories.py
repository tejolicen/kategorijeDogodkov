import os
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn import decomposition, cluster

from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import polyglot
from polyglot.text import Text, Word
import random

_GLAVNE_KATEGORIJE = ['2',     '15',    '5',     '25',  '3',      '38',    '1',        '27',     '18',   '32',     '64',     '36',   '17',      '13',     '28',     '29',         '21',     '53',      '49']
_KATEGORIJE_NAZIVI = ['Music', 'Party', 'Other', 'Art', 'Sports', 'Dance', 'Wellness', 'Health', 'Food', 'Causes', 'Comedy', 'Film', 'Theater', 'Online', 'Crafts', 'Literature', 'Drinks', 'Fitness', 'Networking']

def stripMainCategories(input_file, output_file):
    df = pd.read_csv(input_file, header = 0)
    original_headers = list(df.columns.values)
    data_opis_normalized = df['opis'].astype('U')
    data_kats = df['kategorije_sifre']
    data_katn = df['kategorije_nazivi']
    
    cnt = len(data_katn)
    indexesToRemove = []
    data_kats_new = [None] * cnt
    data_katn_new = [None] * cnt

    for i in range(len(data_kats)):
        kats = data_kats[i]
        only_first_kats = ''
        only_first_katn = ''
        katsArr = kats.split(',')
        for kat in katsArr:
            for j in range(len(_GLAVNE_KATEGORIJE)):
                glavnaKatS = _GLAVNE_KATEGORIJE[j]
                glavnaKatN = _KATEGORIJE_NAZIVI[j]
                if(kat == glavnaKatS):
                    only_first_kats = glavnaKatS
                    only_first_katn = glavnaKatN
                    break
            if(only_first_kats != ''):
                break
        
        if(only_first_kats == ''):  # če nima ene od glavnih kategorij jo pripišemo pod other
            only_first_kats = '5'
            only_first_katn = 'Other'
        if(only_first_kats != ''):
            if(only_first_kats == '28' or only_first_kats == '49' or only_first_kats == '29'): # Crafts, Networking, Literature -> Other
                only_first_kats = '5'
                only_first_katn = 'Other'
            if(only_first_kats == '1' or only_first_kats == '53'): # Wellness, Fitness -> Health
                only_first_kats = '27'
                only_first_katn = 'Health'
            if(only_first_kats == '21'): # Drinks -> Party
                only_first_kats = '15'
                only_first_katn = 'Party'
            if(only_first_kats == '17'): # Theater -> Film
                only_first_kats = '36'
                only_first_katn = 'Film'

            data_kats_new[i] = only_first_kats
            data_katn_new[i] = only_first_katn
        else:
            indexesToRemove.append(i)   # dogodek ne vsebuje ene od glavnih categorij


    df['kategorije_sifre_new'] = data_kats_new
    df['kategorije_nazivi_new'] = data_katn_new
    df.drop(df.index[indexesToRemove], inplace=True)    # dogodke ki ne vsebujejo ene od glavnih kategorij odstranimo
    df.to_csv(output_file, index = False)
    


__file__ = os.getcwd()
dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'scripts\\data\\dogodki50_spucano.csv')
outut_file = os.path.join(dirname, 'scripts\\data\\dogodki50_spucano_glavnekategorije.csv')
stripMainCategories(input_file, outut_file)