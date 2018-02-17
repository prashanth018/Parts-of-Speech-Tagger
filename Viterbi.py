	
TagSet = []
f = open('UniGramCount.txt','r')
content = f.readlines()
f.close()

for i in content:
	TagSet.append(i.split()[0])

#print TagSet
#print len(TagSet)
#l = input()
#TagSet = ["P","V","N","D"]
print "Enter the string"
inp = raw_input()

x = inp.split()

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
	result[i]=0
	
result[n-1] = tag_u
result[n] = tag_v
	
k = n-2
while k>=1:
	result[k] = bp[k+2][result[k+1]][result[k+2]]		
	k-=1	
		
print result[1:]

#print res

#print dp

#print dp[2]["P"]["D"]


