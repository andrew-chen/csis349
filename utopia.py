import protocol
import threading

def sender1(ps):
	while True:
		buffer = protocol.Packet()
		ps.from_network_layer(buffer)
		s = protocol.Frame()
		s.info = buffer
		ps.to_physical_layer(s)

def receiver1(ps):
	while True:
		s = ps.from_physical_layer()
		buffer = s.info
		ps.to_network_layer(buffer)

ps1 = protocol.ProtocolStack()
ps2 = protocol.ProtocolStack()
protocol.establish_physical_connection(ps1,ps2,0.5)

t1 = threading.Thread(target=sender1,args=(ps1,))
t2 = threading.Thread(target=receiver1,args=(ps2,))

t1.start()
t2.start()

input()
