import sys
from copy import copy

class Link(object):
	def __init__(self,node1,node2,distance):
		self.node1 = node1
		self.node2 = node2
		self.distance = distance
	def other_node(self,some_node):
		if self.node1 == some_node:
			return self.node2
		if self.node2 == some_node:
			return self.node1
		sys.exit("tried to get other_node from something other than the given node")

class Node(object):
	def __init__(self,name):
		self.links = []
		self.name = name
		self.routing_table = {} # destination is key, value is (delay,link) pair
	def other_node_on_this_link(self,link):
		return link.other_node(self)

	def update_routing_table(self):
		vectors = {}
		for link in self.links:
			other = other_node_on_this_link(link)
			vectors[id(link)] = {}
			for key,(delay,a_link) in other.routing_table.items():
				vectors[id(link)][key] = delay+link.distance

