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


_SAMPLE_SIZE = 150
original_list = list(data_opis)
sampled_list = random.sample(original_list, _SAMPLE_SIZE)

delezByCountry = []
delezByCountryFilterNoSlov = []

for row in original_list:
    try:
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
                dog[language.code] = dist
        delezByCountry.append(dog)
        if(dog['sl']['confidence'] < 99):
            delezByCountryFilterNoSlov.append(dog)
        
    except:
        print('Preskočen.')


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
        

iNoSlov = len(delezByCountryFilterNoSlov)
slDelezNoSlov = [0] * iNoSlov
enDelezNoSlov = [0] * iNoSlov

slSteviloNoSlov = [0] * iNoSlov
enSteviloNoSlov = [0] * iNoSlov


for i in range(len(delezByCountryFilterNoSlov)):
    if('sl' in delezByCountryFilterNoSlov[i]):
        slDelezNoSlov[i] = delezByCountryFilterNoSlov[i]['sl']['confidence']
        slSteviloNoSlov[i] = delezByCountryFilterNoSlov[i]['sl']['count']
    if('en' in delezByCountryFilterNoSlov[i]):
        enDelezNoSlov[i] = delezByCountryFilterNoSlov[i]['en']['confidence']
        enSteviloNoSlov[i] = delezByCountryFilterNoSlov[i]['en']['count']
        


def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def histogram(x, y = []):
    n_bins = 50

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(x, bins=n_bins)
    if(len(y) > 0):
        axs[1].hist(y, bins=n_bins)

    plt.show()


def scatter_hist(x, y, limBottom, limTop):
    nullfmt = NullFormatter()         # no labels

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
    axScatter.set_xlabel('Slo.(%)', fontsize=15)
    axScatter.set_ylabel('Ang.(%)', fontsize=15)

    # now determine nice limits by hand:
    binwidth = round((limTop - limBottom) / 100)
    xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])

    axScatter.set_xlim((limBottom, limTop))
    axScatter.set_ylim((limBottom, limTop))

    bins = np.arange(limBottom, limTop + binwidth, binwidth)
    axHistx.hist(x, bins=bins)
    axHisty.hist(y, bins=bins, orientation='horizontal')

    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())

    plt.show()




eventDescriptionLengths = []

for row in original_list:
    eventDescriptionLengths.append(len(row))

eventDescriptionLengths_rejectedOutliers = reject_outliers(np.array(eventDescriptionLengths))

histogram(eventDescriptionLengths, eventDescriptionLengths_rejectedOutliers)
#histogram(slStevilo, enStevilo)


scatter_hist(slSteviloNoSlov, enSteviloNoSlov, 0, 2500)


scatter_hist(slDelezNoSlov, enDelezNoSlov, 0, 100, 'Slo.(%)', 'Ang.(%)')