f = open("new_tag.train",'r')
cont = f.readlines()
#print cont
delimiters = [",","\'\'","``","#","$","(",")",".",":","!","!!","!!!","\""]
tags={}
tags["delimiters"]=0
tags["PRP"]=0
tags["WP"]=0
tags["RB"]=0
#tags[""]
for i in cont:
	s = i.split()
	if len(s)==0:
		continue
	if s[-1] in delimiters:
		tags["delimiters"]+=1		
	elif s[-1]=="PRP$":
		tags["PRP"]+=1
	elif s[-1]=="WP$":
		tags["WP"]+=1
	elif s[-1]=="RBR" or s[-1]=="RBS" or s[-1]=="RB" or s[-1]=="WRB":
		tags["RB"]+=1
	
	elif s[-1].split('|') > 1:
		ch = s[-1].split('|')[-1]
		if ch in tags.keys():
			tags[ch]+=1
		else:
			tags[ch]=1
				
	elif s[-1] in tags.keys():
		tags[s[-1]]+=1
	else:	
		tags[s[-1]]=1
f.close()
o = open("Tags_Full","w")

for x in tags.keys():
	li = [x,str(tags[x])]
	o.write(" ".join(li))
	o.write('\n')
o.close()

#Reference https://cs.nyu.edu/grishman/jet/guide/PennPOS.html
