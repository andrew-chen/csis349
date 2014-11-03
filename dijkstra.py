"""
	Dijkstra's algorithm,
	adapted from Tanenbaum's Computer Networks, fifth edition,
	rewritten in Python,
	adapted to be more Pythonic than a direct port
"""

# have dist be a dict where the keys are pairs
dist = {
	(0,0) : 0,
	(0,1) : 1,
	(1,0) : 1,
	(0,2) : 2,
	(2,0) : 2,
	(0,3) : 3,
	(3,0) : 3,
	(1,1) : 0,
	(1,2) : 5,
	(2,1) : 5,
	(1,3) : 6,
	(3,1) : 6,
	(2,2) : 0,
	(2,3) : 7,
	(3,2) : 7,
	(3,3) : 0
}

tentative = "tentative"
permanent = "permanent"
infinity = float("inf") # INFINITY

class State(object):
	# the initializer
	def __init__(self,the_index):
		self.predecessor = None
		self.length = infinity
		self.label = tentative
		self.index = the_index # a value to indicate which one

	# methods for managing and testing for permanent, tentative, and fixing it to permanent
	def fix(self):
		self.label = permanent
	@property
	def tentative(self): return (self.label == tentative)
	@property
	def permanent(self): return (self.label == permanent)

	# getting the list of predecessors
	def predecessors(self):
		curr = self
		while curr is not None:
			yield curr
			curr = curr.predecessor		

def dijkstra(s,dist):
	# infer values of .index from the keys of dist
	index_values = sorted(reduce(lambda x,y: x.union(y),map(set,dist.keys())))
	assert(s in index_values)

	# get our states
	state = [State(i) for i in index_values]

	assert(len(index_values) > 1)
	
	s_node = state[s]
	s_node.length = 0
	s_node.fix()

	current_index = 0
	while True:
		if current_index == s:
			current_index = current_index + 1
		else:
			break

	current_node = state[s]

	for something in range(len(index_values)-1):
		# for each node
		for a_node in state:
			# figure out the distance from the current node to each node
			current_distance = dist[(current_node.index,a_node.index)]

			# if we're already at zero, we don't need to worry about this one
			if current_distance == 0: continue

			# if we've already fixed this one, we don't need to worry about it
			if a_node.permanent: continue

			# figure out what the distance to each node through the current node is
			new_distance = current_node.length + current_distance

			# consider the distance to each node through the current node
			# will going through the current node help us?
			# if not, skip it
			if new_distance >= a_node.length: continue

			# otherwise
			# update the distance to each node and indicate the current node as the predecessor of that
			a_node.length = new_distance
			a_node.predecessor = current_node

		# set the current node to the one that has the shortest path from t so far
		current_node = min([item for item in state if item.tentative],key=lambda x: x.length)

		current_node.fix()

	# figure out the path, starting at s, and then following predecessors
	return {t : [node.index for node in state[t].predecessors()] for t in index_values}


def shortest_path(s,t,dist):
	result = dijkstra(s,dist)
	print result
	return dijkstra(s,dist)[t]

print (shortest_path(3,2,dist))
