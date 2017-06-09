#for getting the parse tree
from nltk.parse.stanford import StanfordParser
from nltk.draw.tree import draw_trees

#for getting POS tags and lemmatizer
from treetagger import TreeTagger

#for getting universal dependencies between the words
import StanfordDependencies

#currently not using lemmatizer

parser = StanfordParser(model_path="/home/pranjal/stanford-parser-full-2016-10-31/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
s = parser.raw_parse("I am not happy but sad",)
draw_trees(list(s)[0])

sd = StanfordDependencies.get_instance(backend='subprocess')
for sentence in s:  
  print "\n".join(map(str,sd.convert_tree(str(sentence))))


tt = TreeTagger(language='english')
print tt.tag('Yolo this day?')

