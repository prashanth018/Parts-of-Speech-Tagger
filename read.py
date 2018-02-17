import re
import Vocab
import math


Rare_word = "Rare"
Numeric = "Numeric"
AllCap = "AllCap"
LastCap = "LastCap"
Delim = "Delimiter"
min_count = 5
TagCount = {}
TriGramCount = {}
BiGramCount = {}
UniGramCount = {}
mp={}
delimiters = [",","\'\'","``","#","$","(",")",".",":",";","%","-","}","{"]
#Yet to be done
TotalCount=0
V = {}
V = Vocab.VocabGenerator()

#Hyper - Parameters
lamb1 = 0.65
lamb2 = 0.25
lamb3 = 0.1

def TagClean(s):
	if s in delimiters:
		return "DLM"		
	elif s=="PRP$":
		return "PRP"
	elif s=="WP$":
		return "WP"
	elif s=="RBR" or s=="RBS" or s=="RB" or s=="WRB":
		return "RB"
	elif s.split('|') > 1:
		ch = s.split('|')[-1]
		return ch
	else:
		return s

def transit(tag,given):
	pp,p = given
	x1 = 0
	x2 = 0
	x3 = 0
	y1 = 0
	y2 = 0
	y3 = 0
	s = " ".join([pp,p,tag])
	if s in TriGramCount:
		x1 = TriGramCount[s]
	s = " ".join([p,tag])
	if s in BiGramCount:
		x2 = BiGramCount[s]
	s = tag
	if s in UniGramCount:
		x3 = UniGramCount[s]
	
	s = " ".join([pp,p])
	if s in BiGramCount:
		y1 = BiGramCount[s]
	s = p
	if s in UniGramCount:
		y2 = UniGramCount[s]	
	y3 = TotalCount
	p1=0
	p2=0
	p3=0
	if y1!=0:
		p1 = lamb1 * (float(x1)/y1)
	if y2!=0:
		p2 = lamb2 * (float(x2)/y2)
	if y3!=0:
		p3 = lamb3 * (float(x3)/y3)
	
	if p1+p2+p3!=0:
		return math.log10(p1+p2+p3)
	else:
		return 0   #this shouldn't be 0.. check what this should be
	
	
	
def emit(word,tag):
	s = " ".join([tag,word])
	x1 = mp[s]
	y1 = V[word]
	if y1!=0:
		p1 = float(x1)/y1
	
	if p1!=0:
		return math.log10(p1)
	else:
		return 0



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



#change.. It is blunder
def WordClean(word):
	if isNum(word):
		return Numeric
	if V[word]>1:
		return word
	x = Rare_word
#	if isAllCap(word):
#		x = AllCap
#	if isLastCap(word):
#		x = LastCap
	if isDelim(word):
		x = Delim
	return x	

'''
TagCount = {}
TriGramCount = {}
BiGramCount = {}
UniGramCount = {}
'''


#All the places below,"DLM" is the symbol for delimiters
#"DLM" => delimiters

f = open('small.train','r')
cont = f.readlines()

#Populating Trigram
j=2
while j<len(cont):
	i=j
	# cont[i]!='\n' and cont[i-1]=='\n'
	if cont[i]=='\n':
		j+=1
		continue
	else:
		pp = "*"
		p = "*"
		while i < len(cont) and cont[i]!="\n":
			s = cont[i].split()[-1]
			s = TagClean(s)
			
			d = " ".join([pp,p,s])
			if d in TriGramCount:
				TriGramCount[d]+=1
			else:
				TriGramCount[d]=1 
			pp=p
			p=s
			i+=1
		
		d = " ".join([pp,p,"STOP"])
		if d in TriGramCount:
			TriGramCount[d]+=1
		else:
			TriGramCount[d]=1
		j=i



#Populating Bigram
j=1
while j<len(cont):
	i=j
	if cont[i]=='\n':
		j+=1
		continue
	else:
		p="*"
		while i<len(cont) and cont[i]!='\n':
			s = cont[i].split()[-1]
			s = TagClean(s)
			
			d = " ".join([p,s])
			if d in BiGramCount:
				BiGramCount[d]+=1
			else:
				BiGramCount[d]=1
			p = s
			i+=1
		d = " ".join([p,"STOP"])
		if d in BiGramCount:
			BiGramCount[d]+=1
		else:
			BiGramCount[d]=1
		j=i
		

#UniGramCount["DLM"]=0
#counter=0
#Populating Unigram
i=0
while i < len(cont):
	if cont[i]=='\n':
		#print i," ",UniGramCount["DLM"]
		i+=1
		continue
	else:
		while i<len(cont) and cont[i]!='\n':
			s = cont[i].split()[-1]
			s = TagClean(s)
			if s not in UniGramCount:
				UniGramCount[s]=1
			else:
				#if s=="DLM":
				#	counter+=1
				UniGramCount[s]+=1
			#print i," ",UniGramCount["DLM"]
			i+=1
		if "STOP" in UniGramCount:
			UniGramCount["STOP"]+=1
		else:
			UniGramCount["STOP"]=1

#print UniGramCount["DLM"]
#print counter


# mp is a dictionary which jeeps track of (tag,word)
for i in cont:
	if i!='\n':
		#print i.split()
		s = i.split()
		x,_ = " ".join(s[:-1]),s[-1]
		x = x.lower()
		x = WordClean(x)
		_ = TagClean(_)
		d = " ".join([_,x])
		if d in mp.keys():	
			mp[d]+=1
		else:
			mp[d]=1

for i in UniGramCount.values():
	TotalCount+=i


ct=0
while i < len(cont):
	if i==0 or i==1:
		i+=1
		continue
	
	splt_cur = cont[i].split()
	splt_prev = cont[i-1].split()
	if len(splt_cur)==0 and len(splt_prev)==0:
		continue
	
	if len(splt_cur)!=0 and len(splt_prev)==0:
		prev_prev = '*'
		prev = '*'
		#cur = " ".join(s[:-1])
		cur = splt_cur[-1]
		Type = Rarewd(splt_cur[:-1].lower())
		'''
		s = " ".join([prev_prev,prev,cur])
		if s in TriGramCount:
			TriGramCount[s]+=1
		else:
			TriGramCount[s]=1
		
		s = " ".join([prev,cur])
		if s in BiGramCount:
			BiGramCount[s]+=1
		else:
			BiGramCount[s]=1
		
		s = " ".join([prev_prev,prev])
		if s in BiGramCount:
			BiGramCount[s]+=1
		else:
			BiGramCount[s]=1
		
		s = prev
		if s in UniGramCount:
			UniGramCount[s]+=1
		else:
			UniGramCount[s]=1
		'''
			
		j=i+1
		while j< 
			
		
	
		
	



























