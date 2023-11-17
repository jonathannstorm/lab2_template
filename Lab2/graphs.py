



class Graph:
    def __init__(self, startVertex=None, valuesDictionary = None, directed=False):
        self._adjacencyList = {}
        if valuesDictionary is None:
            valuesDictionary = {}
        self._valuelist = valuesDictionary
        self._isdirected = directed

    def vertices(self):
        return self._adjacencyList.keys()
    

    def edges(self):
        edges = set()
        for startNode in self._adjacencyList.keys():
            for endNode in self._adjacencyList[startNode]:
                edges.add((min(startNode, endNode), max(startNode, endNode)))
                
        return edges



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
