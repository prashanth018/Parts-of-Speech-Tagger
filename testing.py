import operator
import re
import math
import Vocab

delimiters = [",","\'\'","``","#","$","(",")",".",":",";","%","-","}","{","!","!!","!!!","\""]

#s = raw_input()

#li = s.split()
'''
new_li=[]
for w in li:
	if w[-1] in delimiters:
		new_li.append(w[:-1])
		#new_li.append(w[-1])
	else:
		new_li.append(w)
print new_li
'''

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

#for i in range(len(glob)):
#	print i
#	print glob[i][0]
#	print glob[i][1]
#	print ""

	
	
			
			
			
			
			
			
			
			
			
			
			
						

