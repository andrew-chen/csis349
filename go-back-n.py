import protocol
import threading

MAX_SEQ = 7

def between(a,b,c):
	"Return true if a <= b < c circularly; false otherwise"
	a,b,c = a.value,b.value,c.value
	if (
		((a <= b) and (b < c)) or
		((c < a) and (a <= b)) or
		((b < c) and (c < a))
		):
		return True
	else:
		return False

def send_data(frame_nr,frame_expected,buffer,ps):
	s = protocol.Frame()
	s.info = buffer[frame_nr.value]
	s.seq = frame_nr.copy()
	s.ack = frame_expected.copy().decr()
	ps.to_physical_layer(s)
	ps.start_timer(frame_nr.value)

def protocol5(ps):
	ack_expected = protocol.SequenceNumber(0,MAX_SEQ)
	next_frame_to_send = protocol.SequenceNumber(0,MAX_SEQ)
	frame_expected = protocol.SequenceNumber(0,MAX_SEQ)
	nbuffered = 0

	buffer = map(lambda x:protocol.Packet(),range(MAX_SEQ+1))

	ps.enable_network_layer()

	while True:
		event = ps.wait_for_event()
		if event == protocol.network_layer_ready:
			ps.from_network_layer(buffer[next_frame_to_send.value])
			nbuffered = nbuffered + 1
			send_data(next_frame_to_send,frame_expected,buffer,ps)
			next_frame_to_send.inc()
		elif event == protocol.frame_arrival:
			r = ps.from_physical_layer()
			if r.seq == frame_expected:
				ps.to_network_layer(r.info)
				frame_expected.inc()
			while (between(ack_expected,r.ack,next_frame_to_send)):
				nbuffered = nbuffered-1
				ps.stop_timer(ack_expected.value)
				ack_expected.inc()
		elif event == protocol.timeout:
			next_frame_to_send = ack_expected.copy()
			for i in range(1,nbuffered+1):
				send_data(next_frame_to_send,frame_expected,buffer,ps)
				next_frame_to_send.inc()
		if nbuffered < MAX_SEQ:
			ps.enable_network_layer()
		else:
			ps.disable_network_layer()

ps1 = protocol.ProtocolStack()
ps2 = protocol.ProtocolStack()
ps1.timeout_amount = 3
ps2.timeout_amount = 3
protocol.establish_physical_connection(ps1,ps2,0.1)

t1 = threading.Thread(target=protocol5,args=(ps1,))
t2 = threading.Thread(target=protocol5,args=(ps2,))

t1.start()
t2.start()

input()

