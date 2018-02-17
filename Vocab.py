import operator
import re

Rare_word = "Rare"
Numeric = "Numeric"
AllCap = "AllCap"
LastCap = "LastCap"
Delim = "Delimiter"

def isNum(word):
	if re.match('[0-9]+',word):
		return True
	return False
	
def isDelim(word):
	if re.match('[,]|[\'\']|[``]|[#$)(.:;%]|[\-\{\}]',word):
		return True
	return False
	
def isAllCap(word):
	if re.match('^[A-Z]+$',word):
		return True
	return False

def isLastCap(word):
	if re.match('.*[A-Z]+$',word):
		return True
	return False


def WordClean(word):
	if isNum(word):
		return Numeric
	#if V[word]>1:
	#	return word
	#x = Rare_word
#	if isAllCap(word):
#		x = AllCap
#	if isLastCap(word):
#		x = LastCap
	#if isDelim(word):
	#	return Delim
	return word	



def VocabGenerator():
	f = open('new_new_tag.train','r')
	cont = f.readlines()
	f.close() 
	vocab={}
	for i in cont:
		if i!='\n':
			#print i.split()
			d = i.split()
			x,_ = " ".join(d[:-1]),d[-1]
			x = x.lower()
			x = WordClean(x)
			if x in vocab.keys():	
				vocab[x]+=1
			else:
				vocab[x]=1
	return vocab

'''
voc={}
voc = VocabGenerator()

srt_vocab = sorted(voc.items(), key=operator.itemgetter(1))
f = open('new_vocabulary.txt','w')
for i in srt_vocab:
	x,y = i
	y = str(y)
	d = [x,y]
	f.write(" ".join(d))
	f.write('\n')
f.close()
print "Done"

#print len(vocab.keys())
'''
