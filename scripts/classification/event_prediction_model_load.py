
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

import pickle

sys.path.append(os.path.abspath("extras"))
from textCleaningNLTK import preprocessText

categoryDict = {
    10:'Komedija',
    9:'Zdravje',
    8:'Hrana',
    7:'Dobrodelnost',
    6:'Šport',
    5:'Ostalo',
    4:'Glasba',
    3:'Zabava',
    2:'Veselica',
    1:'Umetnost',
    0:'Film'
}

_PROBA = False

# load the model from disk
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/model.pickle')
filenameTFIDF = os.path.join(dirname, '../data/tfidf.pickle')
if _PROBA:
    filename = os.path.join(dirname, '../data/model_proba.pickle')
    filenameTFIDF = os.path.join(dirname, '../data/tfidf_proba.pickle')
loaded_model = pickle.load(open(filename, 'rb'))
loaded_tfidf = pickle.load(open(filenameTFIDF, 'rb'))

texts = ["""100 KM ROLANJA V ENEM DNEVU. Sprejmeš izziv? 😃
100 km ali ultra 100 km – gre za tradicionalno in še vedno edinstveno rolanje po 100 km dolgi trasi v enem dnevu. 100 km rolanja ni le edinstvena športna izkušnja, ampak tudi preizkušnja samega sebe, kjer nisi časovno omejen, soočiti pa se moraš s svojim pogumom ter fizičnimi in psihičnimi sposobnostmi.
Dogodek je tudi letos namenjen samo članom športnega društva ROLANJE.EU. Držali se bomo vseh aktualnih predpisov za covid-19, četudi to pomeni, da rolamo z 1 km medsebojne razdalje. 😃 Morda pa v najbolj skrajnem primeru celo prek spleta vsak v svoji občini. 😃
🔥 KDAJ: sobota, 18. 9. 2021 ob 8.30
🔥 KJE SE ZBEREMO IN ŠTARTAMO: 8. 30, kolesarsko počivališče Sonček v Mojstrani
🔥 PREDVIDEN ČAS ROLANJA: 100 km oziroma ca. 8 ur
🔥 TRASA: Trasa poteka po dobro poznani in eni izmed najlepših in najbolj varnih rolerskih poti pri nas. Za ogrevanje bomo prvih 10 km rolali v rahel klanec proti Kranjski Gori, nadaljevali mimo Rateč do slovensko-italijanske meje, nato pa nas bo pot vodila v Italijo skozi Trbiž do mesta, kjer bo ura pokazala 50 km. Po kratki pavzi sledi povratek po isti poti do izhodišča. Zadnjih 20 km predstavlja prijeten spust, ki ga zagotovo že vsi komaj čakamo!
🔥 OPREMA: Med rolanjem je OBVEZNA uporaba čelade, ostali ščitniki pa so zelo priporočljivi, še posebej za zapestje. Vsak roleraš naj ima s seboj 1 l tekočine in športno oziroma dovolj kalorično hrano, da ne bo zmanjkalo energije.
Tisti, ki prerolajo 100 km v celoti, dobijo tudi unikatno izdelano medaljo v čast in večni spomin.
Po dogodku je predvideno tudi prijetno druženje nekje ob vodi z možnostjo piknika, zato priporočamo topla oblačila in obutev, piknik dekce, podloge za ležanje, napihljive blazine, kopalke itd"""]
textsCleaned = []
for text in texts:
    preprocessText = preprocessText(text)
    print(preprocessText)
    textsCleaned.append(preprocessText)

if _PROBA:
    text_features = loaded_tfidf.transform(textsCleaned).toarray()
    predictions = loaded_model.predict_proba(text_features)
else:
    text_features = loaded_tfidf.transform(textsCleaned)
    predictions = loaded_model.predict(text_features)

maxPredictionIndex = -1
maxPredictionScore = 0 
# zaenkrat imamo samo 1 prediction naenkrat
if(len(predictions) > 0):
    prediction = predictions[0]
retArr = {}
if _PROBA:
    for idx, feat_pred in enumerate(prediction):
        retArr[categoryDict[idx]] = feat_pred
        if feat_pred > maxPredictionScore:
            maxPredictionIndex = idx
            maxPredictionScore = feat_pred
else:
    maxPredictionIndex = prediction

    

print("  - Predicted as: '{}'".format(categoryDict[maxPredictionIndex]))