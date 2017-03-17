from nltk import tokenize
from sklearn.externals import joblib
from sklearn.naive_bayes import BernoulliNB
import cPickle as pickle
import numpy as np

'''
what i want to do is:
1. take the file name from user
2. then convert it into a list of sentences
3. give each sentence to the classifier
'''


sentences = None
emotions = None
def get_emotions_from_content(content, want_neutral):
	global emotions
	global sentences

	content = content.split('\n')
	#print content
	count = 0
	para = ''
	for i in content:
		para = para + " " + str(i).strip("\n")
	# print para
	sentences = tokenize.sent_tokenize(para)
	# print "***************"
	# for i in sentences:
	# 	print i + "\n"
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
		  print sentences[i] + ": " + emotions[i]