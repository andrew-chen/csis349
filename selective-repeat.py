import protocol
import threading

MAX_SEQ = 7			# should be 2^n - 1
NR_BUFS = (MAX_SEQ + 1)/2

no_nak = True

def init_oldest_frame(ps):
	ps.oldest_frame = MAX_SEQ + 1

def get_oldest_frame(ps):
	try:
		return ps.oldest_frame
	except:
		init_oldest_frame(ps)
		return ps.oldest_frame

def send_frame(fk,frame_nr,frame_expected,buffer,ps):
	global no_nak
	s = protocol.Frame()
	s.kind = fk
	if fk == protocol.data:
		s.info = buffer[frame_nr.value % NR_BUFS]
	s.seq = frame_nr
	s.ack = frame_expected.copy().inc()
	if fk == protocol.nak:
		no_nak = False
	ps.to_physical_layer(s)
	if fk == protocol.data:
		ps.start_timer(frame_nr.value & NR_BUFS)
	ps.stop_ack_timer()

def protocol6(ps):
	r = protocol.Frame()
	out_buf = map(lambda x:protocol.Packet(),range(NR_BUFS))
	in_buf = map(lambda x:protocol.Packet(),range(NR_BUFS))
	arrived = map(lambda x:False,range(NR_BUFS))
	
	ps.enable_network_layer()
	ack_expected = protocol.SequenceNumber(0,MAX_SEQ)
	next_frame_to_send = protocol.SequenceNumber(0,MAX_SEQ)
	frame_expected = protocol.SequenceNumber(0,MAX_SEQ)
	too_far = protocol.SequenceNumber(NR_BUFS,MAX_SEQ)
	nbuffered = 0

	while True:
		event = ps.wait_for_event()
		if event == network_layer_ready:
			nbuffered = nbuffered + 1
			ps.from_network_layer(out_buf[next_frame_to_send.value % NR_BUFS])
			send_frame(protocol.data, next_frame_to_send, frame_expected, out_buf, ps)
			next_frame_to_send.inc()
		elif 
