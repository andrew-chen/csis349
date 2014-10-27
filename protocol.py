import time
import random

MAX_PKT = 1024

class SequenceNumber(object):
	def __init__(self,initial,max):
		assert(initial >= 0)
		assert(max >= 0)
		assert(initial <= max)
		self.value = initial
		self.max = max
	def __eq__(self,other):
		assert(self.max == other.max)
		return (self.value == other.value)
	def inc(self):
		if self.value < self.max:
			self.value = self.value + 1
		else:
			self.value = 0
	def decr(self):
		if self.value == 0:
			self.value = self.max
		else:
			self.value = self.value - 1
		return self
	def copy(self):
		result = SequenceNumber(self.value,self.max)
		return result
	def opposite(self):
		assert(self.max == 1)
		result = self.copy()
		result.value = (1 - result.value)
		return result

class Packet(object):
	def __init__(self,data=""):
		self.data = data
		assert(len(data) < MAX_PKT)

data = "data"
ack = "ack"
nak = "nak"

timeout = "timeout"
frame_arrival = "frame arrival"
network_layer_ready = "network layer ready"

counter = 0

class Frame(object):
	def __init__(self,kind=None,seq=None,ack=None,info=None):
		self.kind = kind
		self.seq = seq
		self.ack = ack
		self.info = info

def establish_physical_connection(ps1,ps2,prob):
	ps1.physical_connection = ps2
	ps2.physical_connection = ps1
	ps1.phys_drop_prob = prob
	ps2.phys_drop_prob = prob
	

class ProtocolStack(object):
	def __init__(self):
		self.event_queue = []
		self.timers = {}
		self.received_frames = []
		self.counter = 0
		self.network_layer_enabled = False
	def wait_for_event(self):
		while True:
			# timeout stuff
			try:
				if time.time() - self.ack_timer > self.timeout_amount:
					self.event_queue.append(timeout)
					del self.ack_timer
			except:
				pass
			for key,value in self.timers.items():
				if time.time() - value > self.timeout_amount:
					self.event_queue.append(timeout)
					del self.timers[key]

			# put network_layer_ready event in queue
			# if the queue is empty
			# and the network_layer is enabled
			if len(self.event_queue) == 0:
				if self.network_layer_enabled:
					self.event_queue.append(network_layer_ready)
			
			# actually getting stuff from the event queue
			if len(self.event_queue):
				result = self.event_queue[0]
				self.event_queue = self.event_queue[1:]
				return result
			else:
				time.sleep(1)

	def from_network_layer(self,p):
		i,c = (id(self),str(self.counter))
		print " "*(i%11)+c+" "*11+" send"
		p.data = (i,c)
		self.counter = self.counter + 1

	def to_network_layer(self,p):
		i,c = p.data
		print " "*(i%11)+c+" "*11+" receive"

	def from_physical_layer(self):
		while 0 == len(self.received_frames):
			pass
		result = self.received_frames[0]
		self.received_frames = self.received_frames[1:]
		return result

	def to_physical_layer(self,s):
		try:
			if random.random() > self.phys_drop_prob:
				self.physical_connection.receive_frame(s)
		except:
			sys.exit("no physical connection")
	def receive_frame(self,s):
		self.event_queue.append(frame_arrival)
		self.received_frames.append(s)

	def start_timer(self,k):
		self.timers[k] = time.time()

	def stop_timer(self,k):
		try:
			del self.timers[k]
		except KeyError:
			pass

	def start_ack_timer(self):
		self.ack_timer = time.time()

	def stop_ack_timer(self):
		try:
			del self.ack_timer
		except:
			pass

	def enable_network_layer(self):
		self.network_layer_enabled = True

	def disable_network_layer(self):
		self.network_layer_enabled = False


