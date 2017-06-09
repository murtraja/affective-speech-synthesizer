from __future__ import print_function


import nltk
from nltk import tokenize
from sklearn.externals import joblib
from sklearn.naive_bayes import BernoulliNB
import cPickle as pickle
import numpy as np
import re
from thread import *

import sys
import csv
import string
import numpy as np
import gensim
from gensim.corpora.dictionary import Dictionary
import pandas as pd

import nltk

from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.metrics import f1_score

from keras.utils import np_utils                    # For encoding
from keras.preprocessing import sequence            # Padding
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dense, Dropout
from keras.models import model_from_json

word2vec = gensim.models.Word2Vec

vocab_dim = 336026                         #2196018 for previous
dim = 300
batch_size = 16
n_epoch = 10
input_length = 50
max_len = 127


def load_files():

    data =[]
    target = []

    with open('/home/pranjal/BE_PROJECT/affective-speech-synthesizer/affect_dataset.csv','rU') as csv_file:
        reader = csv.reader(csv_file,delimiter=",",quotechar='"',dialect=csv.excel_tab)
        for row in reader:
            row[0] = unicode(row[0],errors='ignore')
            data.append(row[0])
            target.append(row[1])

    with open('/home/pranjal/BE_PROJECT/affective-speech-synthesizer/combined_dataset_notweets.csv','rU') as csv_file:
        reader = csv.reader(csv_file,delimiter=",",quotechar='"',dialect=csv.excel_tab)
        for row in reader:
            row[0] = unicode(row[0],errors='ignore')
            data.append(row[0])
            target.append(row[1])

    with open('/home/pranjal/BE_PROJECT/affective-speech-synthesizer/semval_dataset.csv','rU') as csv_file:
            reader = csv.reader(csv_file,delimiter=",",quotechar='"',dialect=csv.excel_tab)
            for row in reader:
                row[0] = unicode(row[0],errors='ignore')
                data.append(row[0]) 
                target.append(row[1])

    with open('/home/pranjal/BE_PROJECT/affective-speech-synthesizer/emo.csv','rU') as csv_file:
            reader = csv.reader(csv_file,delimiter="@",quotechar='"',dialect=csv.excel_tab)
            for row in reader:
                row[0] = unicode(row[0],errors='ignore')
                data.append(row[0])
                target.append(row[1])


    print (len(data))
    return data,target



def any2unicode(text, encoding='utf8', errors='strict'):
    
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text

    return unicode(text.replace('\xc2\x85', '<newline>'), encoding, errors=errors)


gensim.utils.to_unicode = any2unicode





model = gensim.models.KeyedVectors.load_word2vec_format('/home/pranjal/BE_PROJECT/affective-speech-synthesizer/nn/vectors.txt', binary=False)

print("Model loaded")

#print (model.most_similar('good'))


gensim_dict = Dictionary()
gensim_dict.doc2bow(model.vocab.keys(), allow_update=True)
index_dict = {v: k+1 for k, v in gensim_dict.items()}
word_vectors = {word: model[word] for word in index_dict.keys()}


print('Setting up Arrays for Keras Embedding Layer...')
n_symbols = len(index_dict) + 1  # adding 1 to account for 0th index
embedding_weights = np.zeros((n_symbols, dim))
for word, index in index_dict.items():
    embedding_weights[index, :] = word_vectors[word]


print('All okay')


def sentence_to_vectors(sent):

    transformed_train = []
    txt = nltk.word_tokenize(str(sent).lower().replace("'s",'is'))   #More text processing later
    new_txt = []
    for word in txt:
        try:
            new_txt.append(index_dict[word])
        except:
            new_txt.append(0) # Vector of new word is set to 0
    transformed_train.append(new_txt)
    
    return transformed_train



le = preprocessing.LabelEncoder()
data, labels = load_files()
le.fit(labels)
print (le.classes_)

# load json and create model
json_file = open('/home/pranjal/BE_PROJECT/affective-speech-synthesizer/nn/model_1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("/home/pranjal/BE_PROJECT/affective-speech-synthesizer/nn/model_1.h5")
print("Loaded model from disk")


def get_emotions(conn):
    print ("Client connected")
    while True:
        sentence = conn.recv(5000)
        if not sentence:
            break
            
        features = np.array(sentence_to_vectors(sentence))
        features = sequence.pad_sequences(features, maxlen=max_len)
        prediction_values = model.predict(features)
        #print(prediction_values)
        label = prediction_values[0].tolist().index(max(prediction_values[0]))
        #predicted_labels.append(label)
        #print(predicted_labels)
        response = le.inverse_transform(label)
        conn.send(response)
    conn.close()
    print ("Client disconnected")

import socket
import sys

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 4444 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print ('Socket bind complete')
 
#Start listening on socket
s.listen(10)
print ('Socket now listening')

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(get_emotions, (conn,))
        
s.close()




