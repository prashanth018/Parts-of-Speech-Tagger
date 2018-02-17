f = open('tag.train','r')
cont = f.readlines()
f.close()
print len(cont)
i=0
while i < range(len(cont)-1):
	if i==0:
		i+=1
		continue
	if i+1>=len(cont):
		break
	if cont[i-1]!='\n' and cont[i]=='\n' and i+1<len(cont) and cont[i+1]!='\n':
		print i
		del(cont[i])
		i-=1
	i+=1

print len(cont)
f = open('new_tag.train','w')
for x in range(len(cont)):
	f.write(cont[x])
f.close()
