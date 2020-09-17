import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import polyglot
import os
from polyglot.text import Text, Word
from polyglot.mapping import Embedding
from polyglot.detect import Detector

import nltk
from nltk.corpus import stopwords
import numpy as np
import random
from matplotlib.ticker import NullFormatter






__file__ = os.getcwd()
dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'scripts\\data\\dogodki_stripped.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis = df['opis'].astype('U')

original_list = list(data_opis)
_SAMPLE_SIZE = 150
sampled_list = random.sample(original_list, _SAMPLE_SIZE)

delezByCountry = []
delezByCountryFilterNoSlov = []

ponovitevKombinacijeJezika = {}
ponovitevKombinacijeJezikaNatancno = {}

countNapak = 0
for row in original_list:
    try:
        komb_Key = ''
        komb_KeyNatancno = ''
        detector = Detector(str(row), quiet=True)
        dog = {}
        for language in detector.languages:
            if language.code != 'un':
                #print(language)
                dist = {
                "code": language.code,
                "confidence": language.confidence,
                "count": len(str(row)) * (language.confidence / 100)
                }
                komb_Key += (' ' if len(komb_Key) > 0 else '') + language.code
                if language.confidence > 2:
                    komb_KeyNatancno += (' ' if len(komb_KeyNatancno) > 0 else '') + language.code
                dog[language.code] = dist
        delezByCountry.append(dog)
        if(dog['sl']['confidence'] < 99):
            delezByCountryFilterNoSlov.append(dog)
            
        if komb_Key in ponovitevKombinacijeJezika:
            ponovitevKombinacijeJezika[komb_Key] = ponovitevKombinacijeJezika[komb_Key] + 1
        else:
            ponovitevKombinacijeJezika[komb_Key] = 1

        if komb_KeyNatancno in ponovitevKombinacijeJezikaNatancno:
            ponovitevKombinacijeJezikaNatancno[komb_KeyNatancno] = ponovitevKombinacijeJezikaNatancno[komb_KeyNatancno] + 1
        else:
            ponovitevKombinacijeJezikaNatancno[komb_KeyNatancno] = 1
        
    except:
        countNapak = countNapak + 1

print('Število napak: ' + str(countNapak))

ponovitevKombinacijeJezika = {k: v for k, v in sorted(ponovitevKombinacijeJezika.items(), key=lambda item: item[1], reverse=True)}    # sortiramo dictonary
ponovitevKombinacijeJezikaFilter = {}
for key, value in ponovitevKombinacijeJezika.items():
    if value > 1:
        ponovitevKombinacijeJezikaFilter[key] = value

plt.bar(range(len(ponovitevKombinacijeJezikaFilter)), ponovitevKombinacijeJezikaFilter.values(), align='center', tick_label=ponovitevKombinacijeJezikaFilter.values())
xlocs, xlabs = plt.xticks()

for i, v in enumerate(ponovitevKombinacijeJezikaFilter.values()):
    plt.text(xlocs[i] - 0.25, v + 5, str(v))
plt.xticks(range(len(ponovitevKombinacijeJezikaFilter)), list(ponovitevKombinacijeJezikaFilter.keys()), rotation=60)
plt.show()

N = len(delezByCountry)
slDelez = [0] * N
enDelez = [0] * N

slStevilo = [0] * N
enStevilo = [0] * N




for i in range(len(delezByCountry)):
    if('sl' in delezByCountry[i]):
        slDelez[i] = delezByCountry[i]['sl']['confidence']
        slStevilo[i] = delezByCountry[i]['sl']['count']
        
    if('en' in delezByCountry[i]):
        enDelez[i] = delezByCountry[i]['en']['confidence']
        enStevilo[i] = delezByCountry[i]['en']['count']
        

def scatter_hist(x, y, limBottom, limTop, labelX, labelY):
    nullfmt = NullFormatter()        

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(1, figsize=(8, 8))

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)

    # the scatter plot:
    axScatter.scatter(x, y)
    axScatter.set_xlabel(labelX, fontsize=15)
    axScatter.set_ylabel(labelY, fontsize=15)

    # now determine nice limits by hand:
    binwidth = round((limTop - limBottom) / 100)
    xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])

    axScatter.set_xlim((limBottom, limTop))
    axScatter.set_ylim((limBottom, limTop))

    bins = np.arange(limBottom, limTop + binwidth, binwidth)
    axHistx.hist(x, bins=bins, log=True)
    axHisty.hist(y, bins=bins, orientation='horizontal', log=True)

    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())

    plt.show()

print('Scatter histogram DELEŽ JEZIKA V Slo(%)/Ang(%)')
scatter_hist(slDelez, enDelez, 0, 100, 'Slo.(%)', 'Ang.(%)')
