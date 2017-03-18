#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import tokenize
from sklearn.externals import joblib
from sklearn.naive_bayes import BernoulliNB
import cPickle as pickle
import numpy as np

sentences = None
emotions = None


def get_emotions_from_content(content, want_neutral=False):
    global emotions
    global sentences

    content = content.split('\n')
    count = 0
    para = ''
    for i in content:
        para = para + ' ' + str(i).strip('\n')
    sentences = tokenize.sent_tokenize(para)

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