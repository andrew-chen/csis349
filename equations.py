"""
	An attempt to implement, in Python, all the equations found in
	Tanenbaum's "Computer Networks" Fifth Edition
"""
import math

# Chapter 1

# Chapter 2

# implement equations on bottom of page 90 - get a table

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
	while True:
		yield 0
		yield 1

def AMI(iterable):
	current = 0
	for item in iterable:
		if item:
			current = 1 - current
			yield current
		else:
			yield 0

# continue from 126

# Chapter 3

# Chapter 4

# Chapter 5

# Chapter 6

# Chapter 7

