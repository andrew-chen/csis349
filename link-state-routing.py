from routing import Link

import routing

_Node = routing.Node

import dijkstra

class Node(_Node):
	def prepare_routing_table(self):
		try:
			self.sequence_number = self.sequence_number + 1
		except:
			self.sequence_number = 0

		neighbors_info = {}
		for link in self.links:
			neighbor = link.other_node(self)
			neighbors_info[neighbor.name] = (neighbor,link.distance)
		neighbors_info[self.name] = (self,0)
		# 1A. get neighbors
		# 1B. learn neighbors addresses
		# 2. Set distance or cost metric to each neighbor
		# 3. construct packet with all that has been learned
		# 4. Send packet to ALL other routers, including ourselves
		try:
			self.received_packets = self.received_packets
		except AttributeError:
			self.received_packets = {}
		# the following will be us handling it ourselves, and then sending it along to everyone else
		self.process_packet(neighbors_info,self,self.sequence_number)

	def send_along(self,packet,source,sequence_number):
		for link in self.links:
			other = link.other_node(self)
			if other == source:
				continue
			other.receive_packet(packet,source,sequence_number)

	def receive_packet(self,packet,source,sequence_number):
		if source == self:
			return
		try:
			other_packet, other_seq_num, another = self.received_packets[id(source)]
			if sequence_number > other_seq_num:
				self.process_packet(packet,source,sequence_number)
		except KeyError:
			self.process_packet(packet,source,sequence_number)
		except AttributeError:
			self.received_packets = {}
			self.process_packet(packet,source,sequence_number)

	def process_packet(self,packet,source,sequence_number):
		self.received_packets[id(source)] = (packet,sequence_number,source)
		self.send_along(packet,source,sequence_number)
		
	def update_routing_table(self):
		dist = {}
		for packet, seq_num, node in self.received_packets.values():
			for neighbor, distance in packet.values():
				dist[(node.name,neighbor.name)] = distance
				dist[(neighbor.name,node.name)] = distance
		dist[(self.name,self.name)] = 0 # IMPORTANT
		self.routing_table =  dijkstra.dijkstra(self.name,dist)
		
		


if __name__ == "__main__":
        global nodes
        nodes = []
        nodes = [Node("A"),Node("B"),Node("C"),Node("D"),Node("E")]
        for i in range(len(nodes)-1):
                Link(nodes[i],nodes[i+1],1)

        def update():
                global nodes
                for node in nodes:
                        node.prepare_routing_table() # not implemented
                for node in nodes:
                        node.update_routing_table()
        for node in nodes:
                update()
        import pprint
	print "info for A"
        pprint.pprint(nodes[0].routing_table)
        pprint.pprint(nodes[0].links)

