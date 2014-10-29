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
		ps.start_timer(frame_nr.value % NR_BUFS)
	ps.stop_ack_timer()

def protocol6(ps):

	global no_nak

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
		print event
		if event == protocol.network_layer_ready:
			nbuffered = nbuffered + 1
			ps.from_network_layer(out_buf[next_frame_to_send.value % NR_BUFS])
			send_frame(protocol.data, next_frame_to_send, frame_expected, out_buf, ps)
			next_frame_to_send.inc()
		elif event == protocol.frame_arrival:
			r = ps.from_physical_layer()
			print "received frame: "+str((r.kind,r.seq.value,r.ack.value))
			if r.kind == protocol.data:
				if r.seq != frame_expected and no_nak:
					send_frame(protocol.nak,protocol.SequenceNumber(0,MAX_SEQ),frame_expected,out_buf,ps)
				else:
					ps.start_ack_timer()
				if r.seq.between(frame_expected,too_far) and arrived[r.seq.value%NR_BUFS] == False:
					arrived[r.seq.value%NR_BUFS] = True
					in_buf[r.seq.value%NR_BUFS] = r.info
					while (arrived[frame_expected.value%NR_BUFS]):
						ps.to_network_layer(in_buf[frame_expected.value%NR_BUFS])
						no_nak = False
						arrived[frame_expected%NR_BUFS] = False
						frame_expected.inc()
						too_far.inc()
						ps.start_ack_timer()
			if r.kind == protocol.nak and r.ack.copy().inc().between(ack_expected,next_frame_to_send):
				send_frame(protocol.data,r.ack.copy().inc(),frame_expected,out_buf,ps)
			while r.ack.between(ack_expected,next_frame_to_send):
				nbuffered = nbuffered - 1
				ps.stop_timer(ack_expected.value%NR_BUFS)
				ack_expected.inc()
		elif event == protocol.cksum_err:
			if no_nak:
				send_frame(protocol.nak,protocol.SequenceNumber(0,MAX_SEQ),frame_expected,out_buf,ps)
		elif event == protocol.timeout:
			print "timeout is "+str(ps.oldest_frame)
			send_frame(protocol.data,protocol.SequenceNumber(ps.oldest_frame,MAX_SEQ),frame_expected,out_buf,ps)
		elif event == protocol.ack_timeout:
			send_frame(protocol.ack,protocol.SequenceNumber(0,MAX_SEQ),frame_expected,out_buf,ps)
		if nbuffered < NR_BUFS:
			ps.enable_network_layer()
		else:
			ps.disable_network_layer()

ps1 = protocol.ProtocolStack()
ps2 = protocol.ProtocolStack()
ps1.timeout_amount = 3
ps2.timeout_amount = 3
protocol.establish_physical_connection(ps1,ps2,0)

t1 = threading.Thread(target=protocol6,args=(ps1,))
t2 = threading.Thread(target=protocol6,args=(ps2,))

t1.start()
t2.start()

input()

