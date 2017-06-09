LEXICON_FILE = 'nrc.txt'
nrc_hash = {}
line_number = 0
with open(LEXICON_FILE, 'r') as f:
	for line in f:
		
		# ignore the positive and negative emotions
		if line_number%10==5 or line_number%10==6:
			line_number = line_number + 1
			continue;
		#print "now parsing:",line
		(word,emotion,yes) = line.split('\t')
		if int(yes)==1:
			if word not in nrc_hash:
				nrc_hash[word] = []
			nrc_hash[word].append(emotion)
		line_number = line_number + 1
		if line_number%10 == 0:
			# this implies that this word is over
			# check if this word was added to hash
			# if not, then it represents a neutral emotion
			if word not in nrc_hash:
				nrc_hash[word] = ['neutral']
print "NRC lexicon loaded "+str(len(nrc_hash))+" words"