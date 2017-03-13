sentence = "say this angrily"
emotion = 'angry'
EMOTIONS = ['happiness', 'sadness', 'anger', 'fear', 'disgust', 'surprise', 'neutral']

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import sys

def return_xml(sentence, emotion):
	if emotion not in EMOTIONS:
		print "FATAL ERROR! cannot synthesize voice for this emotion"
		sys.exit()

	node_emotionml = Element('emotionml')
	node_emotionml.set("version", "1.0")
	node_emotionml.set("xmlns", "http://www.w3.org/2009/10/emotionml")
	node_emotionml.set("category-set", "http://www.w3.org/TR/emotion-voc/xml#big6")

	if emotion != 'neutral':

		node_emotion = SubElement(node_emotionml, 'emotion')
		node_emotion.text = sentence

		node_category = SubElement(node_emotion, 'category')
		node_category.set("name", emotion)
	else:
		node_emotionml.text = sentence

	return tostring(node_emotionml)

for emotion in ['neutral', 'sadness']:
	print return_xml(sentence, emotion)