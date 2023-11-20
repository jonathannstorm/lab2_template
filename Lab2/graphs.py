
def main():
    wg = WeightedGraph()
    wg.add_vertex(1)


class Graph:
    def __init__(self, startVertex=None, valuesDictionary = None, directed=False):
        self._adjacencyList = {}
        self._valuelist = valuesDictionary
        self._isdirected = directed
        if valuesDictionary is None:
            valuesDictionary = {}
        if startVertex is not None:
            self._adjacencyList[startVertex] = []
        


    def vertices(self):
        return self._valuelist.keys()
    

    def edges(self):
        edges = set()
        for startNode in self._adjacencyList.keys():
            for endNode in self._adjacencyList[startNode]:
                edges.add((min(startNode, endNode), max(startNode, endNode)))
                
        return edges


    def neighbours(self,v):
        neighboutingVertices = self._adjacencyList[v]
        return neighboutingVertices


    def add_edge(self,a,b):
        self.add_vertex(a)

        if b not in self._adjacencyList[a]:
            self._adjacencyList[a].append(b)

        if b not in self._valuelist.keys():
            self.set_vertex_value(b, None)


    def add_vertex(self,a):
        if a not in self._valuelist.keys():
            self._adjacencyList[a] = []
            self.set_vertex_value(a, None)


    def is_directed(self):
        return self._isdirected


    def get_vertex_value(self, v):
        return self._valuelist[v]


    def set_vertex_value(self, v, x):
        self._valuelist[v] = x


class WeightedGraph(Graph):
    def __init__(self, startVertex=None):
        super().__init__(self, startVertex)
        self._weightDictionary = {}


    def set_weight(self, a, b, w):
        pass

    def get_weight(self, a, b):
        pass

if __name__ == '__main__':
    main()