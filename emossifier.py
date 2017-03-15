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
def get_emotions_from_file(filename):
	global emotions
	global sentences
	with open(filename,"rb") as f:
		content = f.readlines()
		content = [x.strip("/n/t ") for x in content]
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

	with open('vectorizer/vectorizer.pkl', 'rb') as fin:
		vectorizer = pickle.load(fin)

	features = vectorizer.transform(sentences)
	print np.shape(features)
	classifier = joblib.load('classifiers/tfidf_svm.pkl')

	emotions = classifier.predict(features).tolist()
	print type(emotions)
	for i in range(len(sentences)):
		print sentences[i] + ": " + emotions[i]
