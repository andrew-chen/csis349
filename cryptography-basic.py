"""
	Utilities for dealing with codes and ascii as lists of 7 bits
"""

def ascii(x):
	assert(len(x) <= 7)
	for i in x:
		assert(i in [0,1])
	if len(x) < 7:
		y = [0 for i in range(7)]
		y[7-len(x):] = x
	else:
		y = x
	return y

def num_to_bits(n):
	assert(n == int(n))
	n = int(n)
	result = []
	while n > 1:
		if n%2:
			result.append(1)
		else:
			result.append(0)
		n = n/2
	result.append(n)
	return list(reversed(result))

def string_to_ascii_bits(s):
	for c in s:
		yield ascii(num_to_bits(ord(c)))

def string_xor(a,b):
	return [[abs(xai-xbi) for xai,xbi in zip(xa,xb)] for xa,xb in zip(a,b)]

if __name__ == "__main__":
	import pprint
	message1 = list(string_to_ascii_bits("I love you."))
	desired_message = list(string_to_ascii_bits("Hello World"))
	pad1 = [
		[1,0,1,0,0,1,0],
		[1,0,0,1,0,1,1],
		[1,1,1,0,0,1,0],
		[1,0,1,0,1,0,1],
		[1,0,1,0,0,1,0],
		[1,1,0,0,0,1,1],
		[0,0,0,1,0,1,1],
		[0,1,0,1,0,1,0],
		[1,0,1,0,1,1,1],
		[1,1,0,0,1,1,0],
		[0,1,0,1,0,1,1]
		]
	ciphertext = string_xor(message1,pad1)
	for char in string_xor(ciphertext,desired_message):
		print char
		print 
