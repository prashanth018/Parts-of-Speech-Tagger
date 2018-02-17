import operator
import re
import math
import Vocab

TriGramCount = {}
BiGramCount = {}
UniGramCount = {}
mp={}
V = {}
V = Vocab.VocabGenerator()
delimiters = [",","\'\'","``","#","$","(",")",".",":",";","%","-","}","{","!","!!","!!!","\""]
TagSet = []

lamb1 = 0.65
lamb2 = 0.25
lamb3 = 0.1

TotalCount=0

#TagSet = ["P","V","N","D"]
#Word Side replacements
Rare_word = "Rare"
Numeric = "Numeric"
AllCap = "AllCap"
LastCap = "LastCap"
Delim = "Delimiter"


#Function for tag side replacements
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
#JJ VBD NN
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
	
	#print "x1 = ",x1
	#print "x2 = ",x2
	#print "x3 = ",x3
	
	s = " ".join([pp,p])
	if s in BiGramCount:
		y1 = BiGramCount[s]
	s = p
	if s in UniGramCount:
		y2 = UniGramCount[s]	
	y3 = TotalCount
	
	#print "y1 = ",y1
	#print "y2 = ",y2
	#print "y3 = ",y3
	
	
	p1=0
	p2=0
	p3=0
	if y1!=0:
		p1 = lamb1 * (float(x1)/y1)
	if y2!=0:
		p2 = lamb2 * (float(x2)/y2)
	if y3!=0:
		p3 = lamb3 * (float(x3)/y3)
	
	#print "p1 = ",p1
	#print "p2 = ",p2
	#print "p3 = ",p3
	
	if p1+p2+p3!=0:
		return math.log10(p1+p2+p3)
	else:
		return -100   #this shouldn't be 0.. check what this should be

def emit(word,tag):
	s = " ".join([tag,word])
	x1 = 0
	y1 = 0
	if s in mp:
		x1 = mp[s]
	if word in V:
		y1 = V[word]
	p1=0	
	#print "x1 ",x1
	#print "y1 ",y1
	if y1!=0:
		p1 = float(x1)/y1
	
	#print "p1 ",p1
	if p1!=0:
		return math.log10(p1)
	else:
		return -100


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
	if isDelim(word):
		return Delim
	return word	



#All the places below,"DLM" is the symbol for delimiters
#"DLM" => delimiters
f = open('new_new_tag.train','r')
cont = f.readlines()
f.close()
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

for i in UniGramCount.values():
	TotalCount+=i

#From here
'''
print len(UniGramCount)
print len(BiGramCount)
print len(TriGramCount)
srt_Uni = sorted(UniGramCount.items(), key=operator.itemgetter(1))
srt_Bi = sorted(BiGramCount.items(), key=operator.itemgetter(1))
srt_Tri = sorted(TriGramCount.items(), key=operator.itemgetter(1))


f = open('UniGramCount.txt','w')
for i in srt_Uni:
	#print i
	f.write(" ".join([i[0],str(i[1]) ] ) )
	f.write('\n')
f.close()


f = open('BiGramCount.txt','w')
for i in srt_Bi:
	f.write(" ".join([i[0],str(i[1]) ] ) )
	f.write('\n')
f.close()


f = open('TriGramCount.txt','w')
for i in srt_Tri:
	f.write(" ".join([i[0],str(i[1]) ] ) )
	f.write("\n")
f.close()
'''
#TO here

f = open('UniGramCount.txt','r')
content = f.readlines()
f.close()

for i in content:
	TagSet.append(i.split()[0])

#print UniGramCount["DLM"]
#print counter
#ct=0
#for i in UniGramCount.values():
#	ct+=i
#print ct,':)'		


#f = open('new_tag.train','r')
#cont = f.readlines()
#f.close()

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

print "Phase-I Done!"
#print transit("NN",("JJ","VBD"))		
#print transit("NN",("*","*"))		

#print "*******************"

#print emit("but","CC")
	
#JJ VBD NN
#CC but

#From here

'''
srt_mp = sorted(mp.items(), key=operator.itemgetter(1))
f = open('map.txt','w')
for i in srt_mp:
	x,y = i
	y = str(y)
	d = [x,y]
	f.write(" ".join(d))
	f.write('\n')
f.close()
print "Writing Map Done"
'''
'''
srt_mp = sorted(mp.items(), key=operator.itemgetter(1))
f = open('map.txt','w')
for i in srt_mp:
	x,y = i
	y = str(y)
	d = [x,y]
	f.write(" ".join(d))
	f.write('\n')
f.close()
print "Done"

'''
'''
vocab={}
for i in cont:
	if i!='\n':
		#print i.split()
		d = i.split()
		x,_ = " ".join(d[:-1]),d[-1]
		x = x.lower()
		x = WordClean(x)
		_ = TagClean(_)
		if x in vocab.keys():	
			vocab[x]+=1
		else:
			vocab[x]=1
return vocab
'''

#to here

#x = raw_input()
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


print "Enter your String"

f = open('test.txt','r')
cont = f.readlines()
f.close()

li = []
ri=[]
ct=0
glob = {}
for i in cont:
	if i=="\n":
		glob[ct] = (li,ri)
		ri=[]
		li=[]
		ct+=1
	else:
		x = i.split()
		#if x[0][-1] in delimiters:
		#	li.append(x[0][:-1])
		#else:
		#	li.append
		li.append(x[0])
		if x[1] in delimiters:
			ri.append("DLM")
		else:
			ri.append(x[1])

ctr=0
glob_ctr=0
for itr in range(len(glob)):
	
	print "Iteration",itr
	#inp = raw_input()
	#x = inp.split()
	x = glob[itr][0]
	S={}
	
	S[-1] = ["*"]
	S[0] = ["*"]
	for i in range(len(x)):
		S[i+1] = TagSet


	#print S

	dp = {}
	bp = {}
	n = len(x)
	#l = 100000
	for k in range(n+1):
		dp[k]={}
		bp[k]={}
		for u in S[k-1]:
			dp[k][u]={}
			bp[k][u]={}
			for v in S[k]:
				dp[k][u][v] = -100000
				bp[k][u][v] = ""
				#l+=1


	dp[0]["*"]["*"] = 0

	#final_tags=[]

	for k in range(1,n+1):
		for u in S[k-1]:
			for v in S[k]:
				val = -10000
				temp_tag=""
				for w in S[k-2]:
					#x = max(x,(dp[k-1][w][u] + transit(v,(w,u)) + emit(x[k],v)) )
					temp = (dp[k-1][w][u] + transit(v,(w,u)) + emit(x[k-1],v))
					if val < temp:
						val = temp
						temp_tag = w
				dp[k][u][v] = val
				bp[k][u][v] = temp_tag

	res = -100000
	tag_u = ""
	tag_v = ""
	for u in S[n-1]:
		for v in S[n]:
			#res = max(res,dp[n][u][v] + transit("STOP",(u,v)) )
			val = dp[n][u][v] + transit("STOP",(u,v))
			if res < val:
				res = val
				tag_u = u
				tag_v = v

	result = []
	for i in range(n+1):
		result.append(0)
	
	result[n-1] = tag_u
	result[n] = tag_v
	
	k = n-2
	while k>=1:
		result[k] = bp[k+2][result[k+1]][result[k+2]]		
		k-=1	
		
	#print result[1:]
	val = ctr
	for act,pred in zip(glob[itr][1],result[1:]):
		if act == pred:
			ctr+=1
	glob_ctr+=len(result[1:])
	print ctr-val,"/",len(result[1:])

print float(ctr)/glob_ctr



