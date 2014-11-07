import sys
from copy import copy

class Link(object):
	def __init__(self,node1,node2,distance):
		self.node1 = node1
		self.node2 = node2
		self.distance = distance
		node1.register_link(self)
		node2.register_link(self)
	def other_node(self,some_node):
		if self.node1 == some_node:
			return self.node2
		if self.node2 == some_node:
			return self.node1
		sys.exit("tried to get other_node from something other than the given node")
	def remove(self):
		self.node1.remove_link(self)
		self.node2.remove_link(self)

class Node(object):
	def __init__(self,name):
		self.links = []
		self.name = name
		self.routing_table = {} # destination is key, value is (delay,link) pair
		global nodes
		for node in nodes:
			self.routing_table[node.name] = (float("inf"),None)
		self.routing_table[name] = (0,None)
		self.preliminary_routing_table = {} # same format as routing table
	def register_link(self,link):
		self.links.append(link)
		self.routing_table[link.other_node(self)] = (link.distance,link)
	def remove_link(self,link):
		assert(link in self.links)
		self.links.remove(link)
		self.links = self.links
		
	def other_node_on_this_link(self,link):
		return link.other_node(self)

	def update_routing_table(self):
		self.routing_table = copy(self.preliminary_routing_table)

	def prepare_routing_table(self):
		vectors_by_link = {}
		#nodes = set()
		global nodes
		neighbors = map(self.other_node_on_this_link,self.links)
		for link in self.links:
			other = self.other_node_on_this_link(link)
			vectors_by_link[id(link)] = {}
			for key,(delay,a_link) in other.routing_table.items():
				if a_link is None:
					vectors_by_link[id(link)][other.name] = link.distance
				else:
					vectors_by_link[id(link)][key] = delay+link.distance
					#nodes.add(link.other_node(self))
		for node in nodes:
			temp_vector = {}
			for link in self.links:
				try:
					temp_vector[id(link)] = vectors_by_link[id(link)][node.name]
				except KeyError:
					temp_vector[id(link)] = float("inf")
			# want minimum delay - after looking up in dict
			# by want the link that is looked up (the key)
			if len(self.links):
				min_dist_link = min(self.links,key=lambda x:temp_vector[id(x)])
				min_dist = temp_vector[id(min_dist_link)]
				self.preliminary_routing_table[node.name] = (min_dist,min_dist_link)
			else:
				# everything is infinity away
				self.preliminary_routing_table[node.name] = (float("inf"),None)
		self.preliminary_routing_table[self.name] = (0,None)

if __name__ == "__main__":
	global nodes
	nodes = []
	nodes = [Node("A"),Node("B"),Node("C"),Node("D"),Node("E")]
	for i in range(len(nodes)-1):
		Link(nodes[i],nodes[i+1],1)
	def update():
		global nodes
		for node in nodes:
			node.prepare_routing_table()
		for node in nodes:
			node.update_routing_table()
	for node in nodes:
		update()
	import pprint
	pprint.pprint(nodes[0].routing_table)
	pprint.pprint(nodes[0].links)
	nodes[0].links[0].remove()
	for i in range(10):
		update()
		pprint.pprint(nodes[1].routing_table)

