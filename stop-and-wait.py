import protocol
import threading
import time

def sender2(ps):
	while True:
		buffer = protocol.Packet()
		ps.from_network_layer(buffer)
		s = protocol.Frame()
		s.info = buffer
		ps.to_physical_layer(s)
		ps.wait_for_event()

def receiver2(ps):
	while True:
		time.sleep(1)
		ps.wait_for_event()
		s = ps.from_physical_layer()
		buffer = s.info
		ps.to_network_layer(buffer)
		ps.to_physical_layer(protocol.Frame())

ps1 = protocol.ProtocolStack()
ps2 = protocol.ProtocolStack()
protocol.establish_physical_connection(ps1,ps2,0)

t1 = threading.Thread(target=sender2,args=(ps1,))
t2 = threading.Thread(target=receiver2,args=(ps2,))

t1.start()
t2.start()

input()
