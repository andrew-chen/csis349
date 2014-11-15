"""
	An attempt to implement, in Python, all the equations found in
	Tanenbaum's "Computer Networks" Fifth Edition
"""
import math
import itertools
import sys

# Chapter 1

# Chapter 2

# implement equations on bottom of page 90 - get a table
def Fourier(sequence_of_bits,amount_of_time):
	number_of_bits = len(sequence_of_bits)
	time_for_one_bit = (1.0*amount_of_time)/number_of_bits
	c = 0
	for bit in sequence_of_bits:
		if bit:
			c = c + time_for_one_bit
	# we have calculated c
	for n in itertools.count(1):
		a_sum = 0
		b_sum = 0
		for k,bit in enumerate(sequence_of_bits):
			start_of_integration = k*time_for_one_bit
			end_of_integration = (k+1)*time_for_one_bit
			a_start = -1*math.cos(2*start_of_integration*n*math.pi/amount_of_time)
			a_end = -1*math.cos(2*end_of_integration*n*math.pi/amount_of_time)
			a_sum = a_sum + ((a_end-a_start)/n*math.pi)
			
			b_start = math.sin(2*start_of_integration*n*math.pi/amount_of_time)
			b_end = math.sin(2*end_of_integration*n*math.pi/amount_of_time)
			b_sum = b_sum + ((b_end-b_start)/n*math.pi)
		yield ( a_sum, b_sum, c )

def Nyquist(bandwidth,number_of_levels):
	return 2 * bandwidth * math.log(number_of_levels,2)

def Shannon(bandwidth,snr):
	return bandwidth * math.log(1+snr,2)

c = 3*pow(10,8) # meters per second

def wavelength(frequency):
	return c/frequency

def frequency(wavelength):
	return c/wavelength

def bit_stream(iterable):
	for item in iterable:
		yield item

nrz = bit_stream

def nrzi(iterable):
	"new iterable has twice as many elements"
	current = 0
	for item in iterable:
		if item:
			yield current
			current = 1 - current
			yield current
		else:
			yield current
			yield current

def Manchester(iterable):
	"new iterable has twice as many elements"
	for item in iterable:
		if item:
			yield 1
			yield 0
		else:
			yield 0
			yield 1

def clock():
	return itertools.cycle([0,1])

def AMI(iterable):
	current = 0
	for item in iterable:
		if item:
			current = 1 - current
			yield current
		else:
			yield 0

dict_of_4b5b = {
	(0,0,0,0) : (1,1,1,1,0)
}
# WORK ABOVE

# continue from 126

# Chapter 3

def same(x,y):
	if x:
		return y
	else:
		return not y

def xor(x,y):
	if x:
		if y: return 0
		return 1
	if y: return 1
	return 0

def Hamming_distance(a,b):
	assert(len(a) == len(b))
	def xor_of_pair(x):
		a,b = x
		return xor(a,b)
	return sum(map(xor_of_pair,zip(a,b)))

def minimum_number_of_Hamming_code_check_bits(m):
	"m <= 2**r - r - 1"
	# return r
	r = 2
	while m > (2**r - r - 1):
		r = r + 1
	return r

def powers_of(x):
	yield 1
	yield x
	y = x*x
	while True:
		yield y
		y = y*x

def is_power_of(x,y):
	powers = power_of(y)
	w = next(powers)
	while x > w:
		w = next(powers)
	if x < y: return False
	if x == y: return True
	sys.exit("should not get here in is_power_of")
		
def as_set_that_would_be_sum_of_powers_of_two(n):
	powers = powers_of(2)
	n = int(n)
	result = []
	for possibility in powers:
		if possibility > n:
			return
		if n%(2*possibility) != 0:
			yield possibility
			n = n - possibility
	
class HammingCode(object):
	def __init__(self,number_of_message_bits):
		self.number_of_message_bits = number_of_message_bits
		self.number_of_check_bits = minimum_number_of_Hamming_code_check_bits(number_of_message_bits)
		self.table = {}
		check_bit_count = 0
		message_bit_count = 0
		for position in range(1,number_of_message_bits+1):
			if is_power_of(position,2):
				self.table[position] = "check"
				check_bit_count = check_bit_count + 1
			else:
				self.table[position] = "message"
				message_bit_count = message_bit_count + 1

def Hamming_encode(x):
	pass

def Hamming_decode(x):
	pass

# Chapter 4

# Chapter 5

# Chapter 6

# Chapter 7

# tests

if __name__ == "__main__":
	print "begin tests"
	if False:
		sequence = [1,0]
		f = Fourier(sequence,2*math.pi)
		print next(f)
		print next(f)
		print next(f)
		print next(f)
	if False:
		print Hamming_distance([0,0,0,0],[1,1,1,1])
		print Hamming_distance([0,1,0,1],[0,1,0,1])
	if True:
		print "testing stuff related to Hamming code"
		print "7 = sum of "+str(list(as_set_that_would_be_sum_of_powers_of_two(7)))
		print "9 = sum of "+str(list(as_set_that_would_be_sum_of_powers_of_two(9)))
		print "10 = sum of "+str(list(as_set_that_would_be_sum_of_powers_of_two(10)))
	print "end tests"
