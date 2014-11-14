"""
	An attempt to implement, in Python, all the equations found in
	Tanenbaum's "Computer Networks" Fifth Edition
"""
import math
import itertools

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

def Hamming_distance(a,b):
	assert(len(a) == len(b))
	# USE zip() HERE
	# WORK HERE

# Chapter 4

# Chapter 5

# Chapter 6

# Chapter 7

# tests

if __name__ == "__main__":
	sequence = [1,0]
	f = Fourier(sequence,2*math.pi)
	print next(f)
	print next(f)
	print next(f)
	print next(f)
