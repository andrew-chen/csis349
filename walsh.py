def dot(a,b):
	assert(len(a)==len(b))
	for i in range(len(a)):
		yield a[i]*b[i]

codes = [
		#[-1,-1,-1,1,1,-1,1,1],
		#[-1,-1,1,-1,1,1,1,-1],
		#[-1,1,-1,1,1,1,-1,-1],
		#[-1,1,-1,-1,-1,-1,1,-1],
		[1,-1,1,-1,1,-1,1,-1],
		[1,1,1,1,1,1,1,1],
		[1,1,-1,-1,1,1,-1,-1],
		[1,-1,-1,1,1,-1,-1,1]
	]

def all_pairs(x):
	for i in range(len(x)):
		for j in range(i):
			yield (x[i],x[j])

def scalar_multiple(s,v):
	for i in v:
		yield s*i

def vector_addition(x,y):
	assert(len(x)==len(y))
	for i in range(len(x)):
		yield x[i]+y[i]

def verify():
	for code in codes:
		print code
		assert(len(code)==sum(dot(code,code)))
	for x,y in all_pairs(codes):
		print (x,y)
		assert(0==sum(dot(x,y)))

	
def prob44chap2ed5ast():
	abc = list(codes[:3])
	abc = list(map(lambda x:list(scalar_multiple(-1,x)),abc))
	print reduce(lambda x,y:list(vector_addition(x,y)),abc)

#prob44chap2ed5ast()
verify()
