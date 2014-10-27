import protocol
import threading

MAX_SEQ = 1

def protocol4(ps):
	next_frame_to_send = protocol.SequenceNumber(0,MAX_SEQ)
	frame_expected = protocol.SequenceNumber(0,MAX_SEQ)
	r = protocol.Frame()
	s = protocol.Frame()
	buffer = protocol.Packet()
	ps.from_network_layer(buffer)
	s.info = buffer
	s.seq = next_frame_to_send.copy()
	s.ack = frame_expected.opposite()
	ps.to_physical_layer(s)
	ps.start_timer(s.seq.value)
	while True:
		event = ps.wait_for_event()
		if event == protocol.frame_arrival:
			r = ps.from_physical_layer()
			if r.seq == frame_expected:
				ps.to_network_layer(r.info)
				frame_expected.inc()
			if r.ack == next_frame_to_send:
				ps.stop_timer(r.ack.value)
				ps.from_network_layer(buffer)
				next_frame_to_send.inc()
		s.info = buffer
		s.seq = next_frame_to_send.copy()
		s.ack = frame_expected.opposite()
		ps.to_physical_layer(s)
		ps.start_timer(s.seq.value)

ps1 = protocol.ProtocolStack()
ps2 = protocol.ProtocolStack()
ps1.timeout_amount = 3
ps2.timeout_amount = 3
protocol.establish_physical_connection(ps1,ps2,0.1)

t1 = threading.Thread(target=protocol4,args=(ps1,))
t2 = threading.Thread(target=protocol4,args=(ps2,))

t1.start()
t2.start()

input()

