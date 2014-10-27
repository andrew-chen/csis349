import protocol
import threading
import time

def sender3(ps):
	buffer = protocol.Packet()
	ps.from_network_layer(buffer)
	next_frame_to_send = 0
	while True:
		s = protocol.Frame()
		s.info = buffer
		s.seq = next_frame_to_send
		print("sending",s.seq)
		ps.to_physical_layer(s)
		print("starting",s.seq)
		ps.start_timer(s.seq)
		event = ps.wait_for_event()
		if event == protocol.frame_arrival:
			s = ps.from_physical_layer()
			print("got ack",s.ack)
			if s.ack == next_frame_to_send:
				print("ack was desired")
				print("stopping",s.ack)
				ps.stop_timer(s.ack)
				ps.from_network_layer(buffer)
				# in stop-and-wait PAR, seq changes as
				next_frame_to_send = 1 - next_frame_to_send

def receiver3(ps):
	s = protocol.Frame()
	frame_expected = 0
	while True:
		time.sleep(1) # should be less than the timeout_amount!
		event = ps.wait_for_event()
		if event == protocol.frame_arrival:
			r = ps.from_physical_layer()
			if r.seq == frame_expected:
				buffer = r.info
				ps.to_network_layer(buffer)
			s.ack = frame_expected
			frame_expected = 1 - frame_expected
			ps.to_physical_layer(s) #indentation important!

ps1 = protocol.ProtocolStack()
ps2 = protocol.ProtocolStack()
ps1.timeout_amount = 3
ps2.timeout_amount = 3
protocol.establish_physical_connection(ps1,ps2,0)

t1 = threading.Thread(target=sender3,args=(ps1,))
t2 = threading.Thread(target=receiver3,args=(ps2,))

t1.start()
t2.start()

input()
