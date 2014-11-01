"""
	Protocol 6 (Selective repeat) accept frames out of order but passes packets to the
	network layer in order. Associated with each outstanding frame is a timer. When the timer
	expires, only that frame is retransmitted, not all the outstanding frames, as in protocol 5
"""
import protocol
import threading

MAX_SEQ = 7			# should be 2^n - 1
NR_BUFS = (MAX_SEQ + 1)/2

no_nak = True			# no nak has been sent yet

# unlike in the book, we don't need an "oldest_frame" variable, but we are keeping track of
# which frame's timer expired

class mod_list(list):
	"""
		This utility class helps us not have to have %NR_BUFS all over the place.
	"""
	def __getitem__(self,which):
		return super(mod_list,self).__getitem__(which%NR_BUFS)
	def __setitem__(self,which,value):
		return super(mod_list,self).__setitem__(which%NR_BUFS,value)

def send_frame(fk,frame_nr,frame_expected,buffer,ps):
	"""
		Construct and send a data, ack, or nak frame
	"""
	global no_nak
	s = protocol.Frame()	# scratch variable
	s.kind = fk		# kind == data, ack, or nak 
	if fk == protocol.data:
		s.info = buffer[frame_nr.value]
	s.seq = frame_nr	# only meaningful for data frames
	s.ack = frame_expected.copy().decr()
	if fk == protocol.nak:
		no_nak = False
	ps.to_physical_layer(s)
	if fk == protocol.data:
		ps.start_timer(frame_nr.value)
	ps.stop_ack_timer()

def protocol6(ps):

	global no_nak

	r = protocol.Frame()
	out_buf = mod_list(map(lambda x:protocol.Packet(),range(NR_BUFS)))
	in_buf = mod_list(map(lambda x:protocol.Packet(),range(NR_BUFS)))
	arrived = mod_list(map(lambda x:False,range(NR_BUFS)))

	def dump():
		for i in range(NR_BUFS):
			ps.println(str(("dump",i,"arrived",arrived[i])))
		for i in range(NR_BUFS):
			ps.println(str(("dump",i,"in_buf",in_buf[i].data)))
		for i in range(NR_BUFS):
			ps.println(str(("dump",i,"out_buf",out_buf[i].data)))
	
	ps.enable_network_layer()
	ack_expected = protocol.SequenceNumber(0,MAX_SEQ)
	next_frame_to_send = protocol.SequenceNumber(0,MAX_SEQ)
	frame_expected = protocol.SequenceNumber(0,MAX_SEQ)
	too_far = protocol.SequenceNumber(NR_BUFS,MAX_SEQ)
	nbuffered = 0

	while True:
		event = ps.wait_for_event()
		if event == protocol.network_layer_ready:
			nbuffered = nbuffered + 1
			ps.from_network_layer(out_buf[next_frame_to_send.value])
			send_frame(protocol.data, next_frame_to_send, frame_expected, out_buf, ps)
			next_frame_to_send.inc()
		elif event == protocol.frame_arrival:
			r = ps.from_physical_layer()
			if r.kind == protocol.data:
				if r.seq != frame_expected and no_nak:
					send_frame(protocol.nak,protocol.SequenceNumber(0,MAX_SEQ),frame_expected,out_buf,ps)
				else:
					ps.start_ack_timer()
				if r.seq.between(frame_expected,too_far) and arrived[r.seq.value] == False:
					arrived[r.seq.value] = True
					in_buf[r.seq.value] = r.info
					while (arrived[frame_expected.value]):
						ps.to_network_layer(in_buf[frame_expected.value])
						no_nak = False
						arrived[frame_expected.value] = False
						frame_expected.inc()
						too_far.inc()
						ps.start_ack_timer()
				else:
					if r.seq.between(frame_expected,too_far):
						pass
					else:
						pass
					if arrived[r.seq.value] == False:
						pass
					else:
						pass
			if r.kind == protocol.nak and r.ack.copy().inc().between(ack_expected,next_frame_to_send):
				send_frame(protocol.data,r.ack.copy().inc(),frame_expected,out_buf,ps)
			while r.ack.between(ack_expected,next_frame_to_send):
				nbuffered = nbuffered - 1
				ps.stop_timer(ack_expected.value)
				ack_expected.inc()
		elif event == protocol.cksum_err:
			if no_nak:
				send_frame(protocol.nak,protocol.SequenceNumber(0,MAX_SEQ),frame_expected,out_buf,ps)
		elif event == protocol.timeout:
			send_frame(protocol.data,protocol.SequenceNumber(event.value,MAX_SEQ),frame_expected,out_buf,ps)
		elif event == protocol.ack_timeout:
			send_frame(protocol.ack,protocol.SequenceNumber(0,MAX_SEQ),frame_expected,out_buf,ps)
		if nbuffered < NR_BUFS:
			ps.enable_network_layer()
		else:
			ps.disable_network_layer()

ps1 = protocol.ProtocolStack()
ps2 = protocol.ProtocolStack()
ps1.timeout_amount = 1
ps2.timeout_amount = 1
protocol.establish_physical_connection(ps1,ps2,0)

t1 = threading.Thread(target=protocol6,args=(ps1,))
t2 = threading.Thread(target=protocol6,args=(ps2,))

t1.start()
t2.start()

input()

