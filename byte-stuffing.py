
def stuff(i):
	for item in i:
		if item in ["ESC","FLAG","SEP"]:
			yield "ESC"
		yield item

def unstuff(i):
	just_saw_ESC = False
	for item in i:
		if item in ["ESC"]:
			if just_saw_ESC:
				yield item
				just_saw_ESC = False
			else:
				just_saw_ESC = True
		else:
			yield item
			just_saw_ESC = False

def frame(header,payload):
	for item in stuff(header):
		yield item
	yield "SEP"
	yield "SEP"
	for item in stuff(payload):
		yield item
	yield "FLAG"
	yield "FLAG"

def extract_frame(source):
	header = []
	body = []
	source = iter(source)
	item = next(source)
	saw_SEP = False
	saw_FLAG = False
	in_what = "header"
	while True:
		if in_what == "header":
			if item is "SEP":
				if saw_SEP:
					in_what = "body"
					saw_FLAG = False
				else:
					saw_SEP = True
			else:
				if saw_SEP:
					header.append("SEP")
				header.append(item)
				saw_SEP = False
		else:
			if item is "FLAG":
				if saw_FLAG:
					return (list(unstuff(header)),list(unstuff(body)))
				else:
					saw_FLAG = True
			else:
				if saw_FLAG:
					body.append("FLAG")
				body.append(item)
				saw_FLAG = False
		if item is "SEP":
			saw_SEP = True
		if item is "FLAG":
			saw_FLAG = True
		item = next(source)

bytes1 = ["A","FLAG","B"]
bytes2 = ["A","ESC","B"]
bytes3 = ["A","ESC","FLAG","B"]
bytes4 = ["A","ESC","ESC","B"]
def test(x):
	print x
	print list(stuff(x))
	print list(unstuff(stuff(x)))

test(bytes1)
test(bytes2)
test(bytes3)
test(bytes4)

frames = [
	frame(bytes1,bytes2),
	frame(bytes2,bytes3),
	frame(bytes3,bytes4),
	frame(bytes4,bytes1)
	]

raw_data = []
for i in frames:
	for j in i:
		raw_data.append(j)
print raw_data

try:
	i = iter(raw_data)
	while True:
		print extract_frame(i)
except StopIteration:
	pass
