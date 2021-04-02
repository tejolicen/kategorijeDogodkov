import pandas as pd
import re
import os
import nltk
from nltk.tokenize import word_tokenize 
import string
import polyglot
from polyglot.text import Text
from polyglot.detect import Detector
#nltk.download()
from textCleaningNLTK import preprocessText





print_output = False


indexesToRemove = []
def odstraniTujeStavke(row):
    returnArray = []
    text = Text(row)
    
    for sentance in text.words: # TODO? sentances
        try:
            odstrani = False
            detector = Detector(str(sentance), quiet=True)
            for language in detector.languages:
                if language.code != 'sl' and language.confidence > 90:
                    odstrani = True
            if not odstrani:
                returnArray.append(sentance)
        except:
            print('Preskočen stavek: ' + sentance)
    return ' '.join(returnArray)

#preverimo delež jezikov v besedilih in primerno sfiltriramo
def preveriJezike(arr):
    sfiltriranArr = []
    i = 0
    for row in arr:
        try:
            detector = Detector(str(row), quiet=True)
            jeSlovenscina = False
            for language in detector.languages:
                if language.code != 'un':
                    if language.code == 'sl':
                        jeSlovenscina = True
                        #če je SLO več kot 90%, pustiš vse
                        if language.confidence >= 90:
                            sfiltriranArr.append(row)
                        #če je SLO več kot 50% in manj kot 90% pa sfiltriraš vse tuje stavke    
                        if language.confidence < 90 and language.confidence >= 50:
                            sfiltriranArr.append(odstraniTujeStavke(row))
                        #če je SLO manj kot 50%, dogodek vržeš vn
                        if language.confidence < 50: 
                            indexesToRemove.append(i)
            if(not jeSlovenscina):
                indexesToRemove.append(i)
        except:
            print('Preskočena vrstica: ' + row)
        i = i + 1
    return sfiltriranArr

indexesToRemove2 = []
def odstraniDogodkeSlabOpis(arr):
    sfiltriranArr = []
    i = 0
    for item in arr:
        word_tokens = word_tokenize(item) 
        if(len(word_tokens) > 10):
            sfiltriranArr.append(item)
        else:
            if(i not in indexesToRemove2):
                indexesToRemove2.append(i)
        i = i + 1
    return sfiltriranArr

def preprocessArray(arr, dodatnoPreverjanje = False):
    ppdArr = []
    for item in arr:
        ppdArr.append(preprocessText(item))

    if(dodatnoPreverjanje):
        ppdArr = preveriJezike(ppdArr)
        ppdArr = odstraniDogodkeSlabOpis(ppdArr)
    
    return ppdArr



dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, '../data/dogodki50.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis = df['opis'].astype('U')
data_naziv = df['naziv'].astype('U')
dataLength = len(data_opis)

print(dataLength)

### Da nazaj shraniš podatk2 ###
data_normalized = preprocessArray(data_opis, True)
naziv_normalized = preprocessArray(data_naziv)





df['nazivpp'] = naziv_normalized
df.drop(df.index[indexesToRemove], inplace=True)
df.drop(df.index[indexesToRemove2], inplace=True)
df['opispp'] = data_normalized
df.to_csv(os.path.join(dirname, '../data/dogodki50_spucano.csv'), index = False)
