class Graph:
    def __init__(self, start=None, values = None, directed=False):
        self._adjlist = {}
        if values is None:
            values = {}
        self._valuelist = values
        self._isdirected = directed
        # plus some code for building a graph from a ’start’ object
        # such as a list of edges
        # here are some of the public methods to implement
    def vertices(self):
    def edges(self):
    def neighbours(self,v):
    def add_edge(self,a,b):
    def add_vertex(self,a):
    def is_directed(self):
    def get_vertex_value(self, v):
    def set_vertex_value(self, v, x):


class WeightedGraph(Graph):

    def set_weight(self, a, b, w):
    def get_weight(self, a, b):
    	# etc etc
    	# check the lab assignment for details
