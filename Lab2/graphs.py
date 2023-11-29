import heapq
import graphviz


class PriorityQueue:
    def __init__(self):
        self._priorityQueue = []        # kön implementeras som en array

    def put(self, element, priority):
        heapq.heappush(self._priorityQueue, (priority, element))    # element med minsta värde läggs till self._priorityQueue[0]

    def get(self):
        if not self.is_empty():
            topPQElement = heapq.heappop(self._priorityQueue)       # self._priorityQueue[0] poppas
            return topPQElement                                     # retur av element med högst prio
        else:
            return None
        
    def is_empty(self):
        return len(self._priorityQueue) == 0
    
    def peek(self):
        if not self.is_empty():
            return self._priorityQueue[0][1]
        else:
            return None
    def size(self):
        return len(self._priorityQueue)
    




def main():
    wg = WeightedGraph()

    wg.add_edge('a', 'b')
    wg.add_edge('a', 'c')
    wg.add_edge('c', 'd')
    wg.add_edge('b', 'd')
    wg.add_edge('c', 'f')
    wg.add_edge('d', 'f')
    wg.add_edge('d', 'e')
    wg.add_edge('g', 'e')
    wg.add_edge('g', 'f')
    wg.add_edge('g', 'h')
    
    print(wg.edges())

    wg.set_weight('a', 'b', 2)
    wg.set_weight('a', 'c', 1)
    wg.set_weight('c', 'd', 1)
    wg.set_weight('b', 'd', 3)
    wg.set_weight('c', 'f', 5)
    wg.set_weight('d', 'f', 1)
    wg.set_weight('d', 'e', 4)
    wg.set_weight('g', 'e', 5)
    wg.set_weight('g', 'f', 1)
    wg.set_weight('g', 'h', 10)






    view_shortest(wg, 'a', 'h', lambda u, v : wg.get_weight(u,v))



def dijkstra(graph, source, cost=lambda u,v: 1):
    # samlare av data
    distanceDicionary = {}
    previousVertex = {}
    vistiedVertices = set()

    # initiera prioritetskön med source så att while loopen kan börja
    priorityQueue = PriorityQueue()
    priorityQueue.put([source, None], 0)


    # while kör tills prioritetskön är tom
    while not priorityQueue.is_empty():
        # element från prioritetskön på formen av en tuple (kostnadHit, [dennaNod, förranoden])
        priorityQueueElement = priorityQueue.get()

        # hämta ut varje parameter från tuplen (kostnadHit, [dennaNod, förranoden])
        currentVertex = priorityQueueElement[1][0]
        backPointer = priorityQueueElement[1][1]
        costToThisNode = priorityQueueElement[0]

        # om currentVertex inte finns i vistitedVertices betyder det att det är första gången vi kommit hit
        # eftersom jag använder mig av en min-prioritetskö där prioriteten är kostaden till noden kan jag vara
        # säker på att detta är den billigaste vägen
        if currentVertex not in vistiedVertices:
            vistiedVertices.add(currentVertex)          # så att vi inte besöker noden igen
            distanceDicionary[currentVertex] = costToThisNode     # spara kostanden hit
            previousVertex[currentVertex] = backPointer # spara vart noden kom ifrån
            
            # lägg till alla grannar till noden på agendan för prioritetskön
            for neighbour in graph.neighbours(currentVertex):
                edgeWeight = cost(str(neighbour), str(currentVertex)) # kostnad mellan nuvarande nod och granne
                costToPreviousVertex = distanceDicionary[currentVertex] # kostnad från source till nuvarande nod
                costToHere = edgeWeight + costToPreviousVertex          # kostnad från source till granne
                
                # prioritetskön uppdateras
                priorityQueue.put([neighbour, currentVertex], costToHere)


    return distanceDicionary, previousVertex



def construct_path_from_previousVertex(prevVertexDict, source, target):
    path = []
    currentVertex = target
    while currentVertex != source:
        path.insert(0, currentVertex)
        currentVertex = prevVertexDict[currentVertex]
    path.insert(0, currentVertex)
    return path

        

    
class Graph:
    def __init__(self, startVertex=None, valuesDictionary = None, directed=False):
        self._adjacencyList = {}
        self._valuelist = valuesDictionary
        self._isdirected = directed
        if startVertex is None:
            pass
        else:
            self._adjacencyList[startVertex] = []

        if self._valuelist is None:
            self._valuelist = {}


    def vertices(self):
        vertices = []
        for key in self._adjacencyList.keys():
            vertices.append(key)
        return vertices
    

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
        self.add_vertex(b)
        if a not in self._adjacencyList[b]:
            self._adjacencyList[b].append(a)
        if b not in self._adjacencyList[a]:
            self._adjacencyList[a].append(b)


    def add_vertex(self,a): 
        if a not in self._adjacencyList.keys():
            self._adjacencyList[a] = []
            self.set_vertex_value(a, None)


    def is_directed(self):
        return self._isdirected


    def get_vertex_value(self, v):
        return self._valuelist[v]


    def set_vertex_value(self, v, x):
        self._valuelist[v] = x


class WeightedGraph(Graph):
    
    def __init__(self):
        super().__init__()
        self._weightDictionary = {}

    def add_edge(self, a, b):
        super().add_edge(a, b)
        self.set_weight(a, b, 0)


    def set_weight(self, a, b, w):
        self.set_weight_key_checker(a, b)
        if b in self._adjacencyList[a]:
            self._weightDictionary[a] = {**self._weightDictionary[a], b: w}
        if a in self._adjacencyList[b]:
            self._weightDictionary[b] = {**self._weightDictionary[b], a: w}
        else:
            print(f'missing edge between {a} and {b}')

    def set_weight_key_checker(self, a, b):
        if a not in self._weightDictionary:
            self._weightDictionary[a] = {}
        if b not in self._weightDictionary:
            self._weightDictionary[b] = {}

    def get_weight(self, a, b):
        return self._weightDictionary[a][b]
    

def visualize(graph, view='dot', name='mygraph', nodecolors=None):
    dot = graphviz.Graph(name = name)

    for vertex in graph.vertices():
        if vertex not in nodecolors:
            dot.node(
                str(vertex),
                fillcolor = 'white',
                style = 'filled'
            )
        else:
            dot.node(
                str(vertex),
                fillcolor = 'orange',
                style = 'filled'
            )

    
    for (v, w) in graph.edges():
        dot.edge(str(v), str(w))

    dot.render(view=True)

    








def view_shortest(G, source, target, cost = lambda u,v: 1):
    distances, prevVertexes = dijkstra(G, source, cost)

    path = construct_path_from_previousVertex(prevVertexes, source, target)
    

    print(path)
    print('\n')
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)



if __name__ == '__main__':
    main()