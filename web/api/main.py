import sys
import os
import shutil
import time
import traceback

from flask import Flask, request, jsonify
import pandas as pd
import pickle
from textCleaningNLTK import preprocessText

app = Flask(__name__)

# inputs

categoryDict = {
    10:'Komedija',
    9:'Zdravje',
    8:'Hrana',
    7:'Dobrodelni nameni',
    6:'Šport',
    5:'Ostalo',
    4:'Glasba',
    3:'Žurke',
    2:'Veselica',
    1:'Umetnost',
    0:'Film'
}




model_directory = 'model'
model_file_name = '%s/model.pickle' % model_directory
tfidf_file_name = '%s/tfidf.pickle' % model_directory

# These will be populated at training time
model_columns = None
loaded_model = None
loaded_tfidf = None

print('Hey, we started!')


def loadModels():
    global loaded_model
    global loaded_tfidf
    ret_text = ''
    try:
        loaded_model = pickle.load(open(model_file_name, 'rb'))
        ret_text = 'Model loaded. '
        loaded_tfidf = pickle.load(open(tfidf_file_name, 'rb'))
        ret_text = ret_text + 'TFIDF loaded.'
    except Exception as e:
        ret_text = 'No model here, train first. ' + str(e)
        loaded_model = None
        loaded_tfidf = None

    print(ret_text)
    return ret_text

@app.route('/predict', methods=['GET'])
def predictGET():
    return 'Obvezen klic POST!'

@app.route('/predict', methods=['POST'])
def predictPOST():
    if loaded_model:
        try:
            print('Predict!')
            dataText = request.data.decode('utf-8')
            
            textsCleaned = []
            preprocessedText = preprocessText(dataText)
            print(preprocessedText)
            textsCleaned.append(preprocessedText)
            #textsCleaned.append(dataText)
            text_features = loaded_tfidf.transform(textsCleaned)
            predictions = loaded_model.predict_proba(text_features)
            print(predictions)
            # Converting to int from int64
            return jsonify({
                    "prediction": categoryDict[predictions[0]],
                    "ppText": preprocessedText
                    })

        except Exception as e:

            return jsonify({'error': str(e), 'trace': traceback.format_exc()})
    else:
        return loadModels()



if __name__ == '__main__':
    loadModels()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=True)

