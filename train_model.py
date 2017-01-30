import re
import nltk
import random
import itertools
import csv
import sys
import os
import cPickle as pickle

import pandas as pd
import numpy as np

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_selection.univariate_selection import SelectKBest, chi2, f_classif
from sklearn import cross_validation
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import normalize, binarize, LabelBinarizer
from sklearn.ensemble import RandomForestClassifier
english_stemmer = nltk.stem.SnowballStemmer('english')
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
def sentence_to_wordlist( temp, remove_stopwords=True, lemmatize=True ):

	#print "now converting sentence",temp,"to word list"
	text = re.sub("[^a-zA-Z]"," ", temp)
	#print text
	words = text.lower().split()
	
	if remove_stopwords:
		stops = set(stopwords.words("english"))
		words = [w for w in words if not w in stops]
	if lemmatize:
		words = [lmtzr.lemmatize(w) for w in words]
	b=[]
	# If stemming is to be used
	stemmer = english_stemmer
	for word in words:
		b.append(stemmer.stem(word))
	#print b
	
	#print words
	#sys.exit(0)
	return(words)
def load_file(filename, data, target):
	with open(filename,'rU') as csv_file:
		reader = csv.reader(csv_file,delimiter=",",quotechar='"',dialect=csv.excel_tab)
		for row in reader:
			data.append(" ".join(sentence_to_wordlist(row[0])))
			target.append(row[1])
def load_files():
	data =[]
	''' this list will hold the sentence with punctuation (and stopwords) removed'''
	target = []
	'''this list will contain the correspoding emotion of the above data list'''
	files = ['affect_dataset.csv', 'combined_dataset.csv', 'semval_dataset.csv']
	for f in files:
		load_file(f, data, target)
	print len(data)
	return data,target


def preprocess(data,target):
	
	vectorizer = TfidfVectorizer(use_idf = True,max_features = 5000,ngram_range=(1,2),analyzer='word',lowercase=True)
	transformed_data = vectorizer.fit_transform(data)
	#print transformed_data
	#print vectorizer.get_feature_names()
	#idf = vectorizer.vocabulary_
	#print dict(zip(vectorizer.get_feature_names(), idf))
	
	with open('vectorizer/vectorizer.pkl', 'wb') as fin:
		pickle.dump(vectorizer, fin)

	return transformed_data, target


def learn_model(data,target):

	#print data
	data_train,data_test,target_train,target_test = cross_validation.train_test_split(data,target,test_size=0.20,random_state=0)
	print len(target_train)
	print "*********************************************************************************"
	print len(target_test)
	classifier = RandomForestClassifier().fit(data_train,target_train)
	joblib.dump(classifier, 'classifiers/tfidf_nb.pkl')
	
	predicted = classifier.predict(data_test)
	
	evaluate_model(target_test,predicted)
	'''
	model = RandomForestClassifier(n_estimators=100)
	#Simple K-Fold cross validation. 10 folds.
	cv = cross_validation.KFold(data.shape[0], n_folds=10)
	results = []
	# "Error_function" can be replaced by the error function of your analysis
	for traincv, testcv in cv:
		print traincv
		print testcv
		print type(testcv)
		print type(data)
		probas = model.fit(data[traincv], target[traincv]).predict_proba(data[testcv])
		results.append( accuracy_score(target[testcv], model.predict(data[testcv])) )
	print "Results: " + str( np.array(results).mean() )
	'''


def evaluate_model(target_true,target_predicted):
	print "The accuracy score is {:.2%}".format(accuracy_score(target_true,target_predicted))
	y_actu = pd.Series(target_true, name='Actual')
	y_pred = pd.Series(target_predicted, name='Predicted')
	df_confusion = pd.crosstab(y_actu,y_pred)
	print df_confusion
	#print confusion_matrix(target_true, target_predicted,labels = ['anger', 'joy', 'neutral', 'sadness', 'surprise'])

if __name__ == "__main__":

	data, target = load_files()
	features, labels = preprocess(data,target)
	learn_model(features,labels)