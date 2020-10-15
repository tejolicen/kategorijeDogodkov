from __future__ import print_function
import pyLDAvis
import pyLDAvis.sklearn
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import numpy as np
from sklearn import datasets, cluster
import os

sub_category = ['comp.sys.mac.hardware', 'rec.autos', 'sci.space', 'misc.forsale', 'talk.politics.guns', 'talk.religion.misc']
newsgroups = fetch_20newsgroups(categories=sub_category, remove=('headers', 'footers', 'quotes'))
docs_raw = newsgroups.data
print(len(docs_raw))


dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'data/dogodki_strippedOnlySlov.csv')
df = pd.read_csv(input_file, header = 0)
original_headers = list(df.columns.values)
data_opis_normalized = df['opis'].astype('U')




tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                #stop_words = 'english',
                                lowercase = True,
                                token_pattern = r'\b[a-zA-Z]{3,}\b',
                                max_df = 0.5, 
                                min_df = 10)
dtm_tf = tf_vectorizer.fit_transform(data_opis_normalized)
print(dtm_tf.shape)


#agglo = cluster.FeatureAgglomeration(n_clusters=24)
#agglo.fit(data_opis_normalized)
#X_reduced = agglo.transform(data_opis_normalized)

tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
dtm_tfidf = tfidf_vectorizer.fit_transform(data_opis_normalized)
print(dtm_tfidf.shape)



# for TF DTM
lda_tf = LatentDirichletAllocation(n_components=8, random_state=0)
lda_tf.fit(dtm_tf)
# for TFIDF DTM
lda_tfidf = LatentDirichletAllocation(n_components=8, random_state=0)
lda_tfidf.fit(dtm_tfidf)


def get_dominant_topic(ldamodel, corpus, data):
    sent_topics_df = pd.DataFrame()

    arT = ldamodel[corpus]

    for i, row in enumerate(arT):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), 
                                                                  round(prop_topic,4), 
                                                                  topic_keywords]), 
                                                       ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    sent_topics_df = pd.concat([sent_topics_df, data['Abstract'], data['Title']], axis=1)
    sent_topics_df.reset_index(inplace=True)
    sent_topics_df.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text', 'Title']
    return sent_topics_df

    
dominant_topic = get_dominant_topic(lda_tf, dtm_tf, data_opis_normalized)


visualisation = pyLDAvis.sklearn.prepare(lda_tf, dtm_tf, tf_vectorizer)
pyLDAvis.save_html(visualisation, os.path.join(dirname, 'output/LDA_Visualization_CountVectorizer.html'))

#visualisation = pyLDAvis.sklearn.prepare(lda_tfidf, dtm_tfidf, tfidf_vectorizer)
#pyLDAvis.save_html(visualisation, os.path.join(dirname, 'output/LDA_Visualization_TfidfVectorizer.html'))

#visualisation = pyLDAvis.sklearn.prepare(lda_tfidf, dtm_tfidf, tfidf_vectorizer)
#pyLDAvis.save_html(visualisation, os.path.join(dirname, 'LDA_Visualization_AGGLO.html'))


