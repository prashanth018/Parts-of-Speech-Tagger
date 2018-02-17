
f1 = open("treebank3_sect2.txt","r")
f2 = open("tag.train","w")

content = f1.readlines()
#print content
#d = input()
for x in content:
	temp = x.split()
	#print temp
	#d = input()
	if len(temp)==0:
		f2.write("\n")
		continue
	elif "=" in x:
		f2.write("\n")
		continue
	
	for mp in temp:
		if mp!='[' and mp!=']':
			#word,tag = mp.split('/')
			f2.write(" ".join(mp.split('/')) )
			f2.write("\n")
f2.write('\n')			
	
f1.close()
f2.close()

