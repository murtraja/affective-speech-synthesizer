#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import tokenize
from sklearn.externals import joblib
from sklearn.naive_bayes import BernoulliNB
import cPickle as pickle
import numpy as np
import kb
import socket
import time

import  emotion_identifier as ei
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
import csv
import pandas as pd
#import numpy as np

import sys


sentences = None
emotions = []

negation = {"won't":"will not",
            "can't":"can not",
            "don't":"do not",
            '"don\'t':'do not',
            "didn't":"did not",
            "doesn't":"does not",
            "couldn't":"could not",
            "wouldn't":"would not",
            "shan't":"shall not",
            "wasn't":"was not",
            "wasn't,":"was not,",
            "hadn't":"had not",
            "hasn't":"has not",
            "haven't":"have not",
            "weren't":"were not",
            "shouldn't":"should not",
            "aren't":"are not",
            "isn't":"is not",
            '"isn\'t':"is not",
            "Don't":"Do not",
            "Ain't":"Am not",
            "ain't":"am not"}
#ain't is ambigiuos


def get_emotions_from_content(content, want_neutral=False):
    global emotions
    global sentences
    
    
    content = content.split('\n')
    count = 0
    para = ''
    for i in content:
        para = para + ' ' + str(i).strip('\n')
    sentences = tokenize.sent_tokenize(para)
    #print sentences

    for i in range(len(sentences)):
      print i
      x = sentences[i].split()
      flag = False
      for j in range(len(x)):
        #print i[j]
        if "n't" in x[j]:
          x[j] = negation[x[j]]
          flag = True
        if "not"==x[j]:
          flag = True
      sentences[i] = ' '.join(x)
      if flag:
        #send to Kb
        emotions.append(str(kb.startKB(sentences[i])))
      else:
        #send to lstm
        s.send(sentences[i])
        emotions.append(str(s.recv(2000)))
      print "len: "+str(len(emotions))
      
    s.close()
    '''
    x = content.split()
    flag = False
    for j in range(len(x)):
      #print i[j]
      if "n't" in x[j]:
        x[j] = negation[x[j]]
        flag = True
      if "not"==x[j]:
        flag = True
    content = ' '.join(x)
    if flag:
      #send to Kb
      emotions.append(str(kb.startKB(content)))
    else:
      #send to lstm
      s.send(content)
      emotions.append(str(s.recv(2000)))
    print "len: "+str(len(emotions))
    
     
    if not want_neutral:
        with open('vectorizer/vectorizer.pkl', 'rb') as fin:
            vectorizer = pickle.load(fin)

        features = vectorizer.transform(sentences)
        print np.shape(features)
        classifier = joblib.load('classifiers/tfidf_svm.pkl')

        emotions = classifier.predict(features).tolist()
        print type(emotions)
    else:
        emotions = ['neutral' for _ in range(len(sentences))]

    for i in range(len(sentences)):
        print sentences[i] + ': ' + emotions[i]
   '''


'''
##################This has to be removed!

def evaluate_model(target_true,target_predicted):
	print "The accuracy score is {:.2%}".format(accuracy_score(target_true,target_predicted))
	y_actu = pd.Series(target_true, name='Actual')
	y_pred = pd.Series(target_predicted, name='Predicted')
	df_confusion = pd.crosstab(y_actu,y_pred)
	print df_confusion

def load_file(filename, data, target):
	with open(filename,'rU') as csv_file:
		reader = csv.reader(csv_file,delimiter=",",quotechar='"',dialect=csv.excel_tab)
		for row in reader:
			data.append(unicode(row[0],errors='ignore'))
			target.append(row[1])

def load_files():
	data =[]
	#this list will hold the sentence with punctuation (and stopwords) removed
	target = []
	#this list will contain the correspoding emotion of the above data list
	files = ['affect_dataset.csv', 'combined_dataset_notweets.csv', 'semval_dataset.csv']
	for f in files:
		load_file(f, data, target)
	#print len(data)
	return data,target

data,labels = load_files()
data_train,data_test,target_train,target_test = cross_validation.train_test_split(data,labels,test_size=0.20,random_state=15)

predicted=[]
'''

#create a socket
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 4444 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

print "Now waiting for LSTM server...",
sys.stdout.flush()

while True:
    try:
        s.connect((HOST,PORT))
        break
    except:
        print ".",
        sys.stdout.flush()
        time.sleep(1)
        continue
        
print "\nConnected to LSTM server"
sys.stdout.flush()
#################################################################
'''
for sentence in data_test:
  get_emotions_from_content(sentence)
'''

#evaluate_model(target_test,emotions)


   
#get_emotions_from_content("very can't be a good boy. But does some bad things. I like her.\n Hello world. This is best.")
