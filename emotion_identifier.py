from nrclexicon import nrc_hash
import nltk, string
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
import nltk.data
from operator import itemgetter
from collections import Counter
import codecs

stemmer = EnglishStemmer()

required_emotion = ['joy', 'surprise', 'neutral', 'anger', 'sadness']
def find_dominant_emotion(emotion_list):
	
	emotion_list = [emo for emo in emotion_list if emo in required_emotion]
	#print 'received emotion list as', emotion_list
	if emotion_list == []:
		return "neutral"
	emotion_dict = dict(Counter(emotion_list))
	#print "emotion_dict:", emotion_dict
	emotion_sorted = sorted(emotion_dict.items(), key=itemgetter(1), reverse=True)
	#print "emotion_sorted:", emotion_sorted
	likely_emotion = emotion_sorted[0][0]
	# now if you don't like neutral, remove it or send it
	if likely_emotion=='neutral' and len(emotion_sorted)>1:
		return emotion_sorted[1][0]
	'''
	one more thing that needs to be considered here is that
	if there are emotions which we don't care about, then
	replace them with appropriate ones which we do care about
	'''
	return likely_emotion

def get_emotion_from_features(features):
	emotion_list = []
	for feature in features:
		if feature in nrc_hash:
			#print nrc_hash[feature]
			emotion_list = emotion_list + nrc_hash[feature]
		else:
			# try one more time, but with stemmed result
			stemmed = stemmer.stem(feature)
			original_feature = feature
			feature = str(stemmed)
			if feature in nrc_hash:
				#print "stemmed",original_feature,"to",feature,"having emotion",nrc_hash[feature]
				emotion_list = emotion_list + nrc_hash[feature]
	return find_dominant_emotion(emotion_list)

def get_features_from_sentence(sentence):
	#sentence = sentence.translate(None, string.punctuation)
	'''
	the problem here is that you're becomes youre
	so might consider removing stop words before
	and after removal of punctuation
	'''

	tokens = nltk.word_tokenize(sentence)
	#features = [x for x in map(str.lower,tokens) if x not in stopwords.words('english')]
	return tokens

def get_emotion_from_sentence(sentence):
	features = get_features_from_sentence(sentence)
	#print "features:",features
	emotion = get_emotion_from_features(features)
        if emotion not in required_emotion:
            emotion = 'neutral'
	return emotion


'''
stop words
i me my myself we our ours ourselves you your yours yourself yourselves he him his himself she her hers herself it its itself they them their theirs themselves what which who whom this that these those am is are was were be been being have has had having do does did doing a an the and but if or because as until while of at by for with about against between into through during before after above below to from up down in out on off over under again further then once here there when where why how all any both each few more most other some such no nor not only own same so than too very s t can will just don should now d ll m o re ve y ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn
'''
