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

	def neighbors(self):
		return map(self.other_node_on_this_link,self.links)

