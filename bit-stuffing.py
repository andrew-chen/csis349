bits = [0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0]

def stuff(bs):
	bs = iter(bs)
	count1 = 0
	while True:
		b = next(bs)
		yield b
		if b == 1:
			count1 = count1 + 1
			if count1 >= 5:
				print "yielding 0"
				yield 0
				count1 = 0
		else:
			count1 = 0

def unstuff(bs):
	bs = iter(bs)
	count1 = 0
	while True:
		b = next(bs)
		if b == 1:
			count1 = count1 + 1
			if count1 >= 5:
				next_bit = next(bs)
				print ("lookahead",next_bit)
				if next_bit == 0:
					count1 = 0
					print "unstuffing"
				else:
					print "flag"
					yield "flag"
				count1 = 0
		else:
			count1 = 0
		yield b

print bits
stuffed = list(stuff(bits))
print stuffed
unstuffed = list(unstuff(stuffed))
print unstuffed

