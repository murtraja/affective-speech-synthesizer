#for getting the parse tree
from nltk.parse.stanford import StanfordParser
from nltk.draw.tree import draw_trees

#for getting POS tags and lemmatizer
#from treetagger import TreeTagger

#for getting universal dependencies between the words
import StanfordDependencies
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

import  emotion_identifier as ei
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
import csv
import pandas as pd
import numpy as np

strong_qualifying_words = ['very','extremely','huge','great']
average_qualifying_words = ['hardly','quite']
low_qualifying_words = ['little','less']

def calc_score(sentence,emo):
  if emo:
    answer_emotion = "neutral"
    emo_dict = {"joy":0, "sadness":0, "surprise":0, "anger":0, "neutral":0}

    parser = StanfordParser(model_path="/home/pranjal/stanford-parser-full-2016-10-31/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    
    #generate listiterator object
    s = parser.raw_parse(sentence,)
    
    #draw_trees(list(s)[0])

    #parsed_tree = list(s)
    #print parsed_tree  
    
    #object to use convert_tree() function
    #for using further
    sd = StanfordDependencies.get_instance(backend='subprocess')
    tree_token = ()
    for x in s:  
      tree_token = sd.convert_tree(str(x))
      
    print tree_token
    
    index_dict = {}
    get_index = 0
    
    for key in emo.keys():
      emo_dict[emo[key]]+=20
      
      for j in range(len(tree_token)):
        if tree_token[j].form == key:
          get_index = tree_token[j].index
          break

      for j in range(len(tree_token)):
        if tree_token[j].deprel == 'amod' or tree_token[j].deprel == 'advmod':
          if tree_token[j].head == get_index:
            if tree_token[j].form in strong_qualifying_words:
                  emo_dict[emo[key]]+=100
            elif tree_token[j].form in average_qualifying_words:
                  emo_dict[emo[key]]+=50
      
      index_dict[key]=get_index
    
    #print emo_dict
    #print index_dict  
    total = -1
    
    #Do not consider neutral emotion values as
    #they might be significantly higher than the
    #other emotions because of more words being
    #neutral. Also, they cannot be removed because the negation
    #sometimes works upon the neutral words (eg. I do not think ...)
    for key in emo_dict.keys():
      if emo_dict[key] > total and key!="neutral" and emo_dict[key] != 0:
        answer_emotion = key
        total = emo_dict[key]

    if total == -1:
      return "neutral"
    
    else:
      #check for negation      
      for j in range(len(tree_token)):
        if tree_token[j].deprel == 'neg':
          if tree_token[j].head in index_dict.values():
            if total > 20:
              answer_emotion="neutral"
            elif total == 20:
              if answer_emotion=="joy":
                answer_emotion="sadness"
              elif answer_emotion=="sadness":
                answer_emotion="joy"
              else:
                answer_emotion="neutral"
    
      return answer_emotion

  else:
    return "neutral"
  

def get_lemmatized_form(word):
    lemmatized_word = wordnet_lemmatizer.lemmatize(word)
    #print lemmatized_word
    return lemmatized_word
    
    
def get_word_emotion_dictionary(sentence):
  word_emotion_dictionary = {}
  for word in sentence.split(' '):
    word = word.strip('.!?')    
    word = get_lemmatized_form(word)
    word_emotion_dictionary[word] = ei.get_emotion_from_sentence(word)
  return word_emotion_dictionary

def startKB(sentence):
  words = sentence.split()
  for i in range(len(words)):
    words[i] = unicode(words[i],errors='ignore')
  sentence = " ".join(words)
  tt = TreeTagger(language='english')
  pos = tt.tag(sentence)
  #print pos[0][1]
  dic = []
  array = ['JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']
  for i in range(len(pos)):
    if pos[i][1] in array:
      dic.append(pos[i])
  #print dic  
  
  emo = get_word_emotion_dictionary(sentence)
  #print emo  
  return calc_score(sentence,emo)


'''
This has to be removed!

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
			data.append(row[0])
			target.append(row[1])

def load_files():
	data =[]
	 this list will hold the sentence with punctuation (and stopwords) removed
	target = []
	this list will contain the correspoding emotion of the above data list
	files = ['affect_dataset.csv', 'combined_dataset_notweets.csv', 'semval_dataset.csv']
	for f in files:
		load_file(f, data, target)
	#print len(data)
	return data,target

data,labels = load_files()
data_train,data_test,target_train,target_test = cross_validation.train_test_split(data,labels,test_size=0.20,random_state=15)

predicted=[]
for sentence in data_test:
  string = startKB(sentence)
  predicted.append(string)

evaluate_model(target_test,predicted)
'''

#startKB("I am not very happy.")
