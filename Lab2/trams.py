import sys
sys.path.append("./Lab1/")
import tramdata as td
import graphs as g
import json


TRAM_LINES = './Lab1/data/tramlines.txt'
TRAM_STOPS = './Lab1/data/tramstops.json'

TRAM_FILE = './tramnetwork.json'

td.build_tram_network(TRAM_STOPS, TRAM_LINES)

def main():
    
    tramGraph = g.WeightedGraph()


    with open(TRAM_FILE, 'r') as tramfile:
        tramNet = json.load(tramfile)

        linesDictionary = tramNet['lines']
        stopDictionary = tramNet['stops']




        for line in linesDictionary.keys():
            for stopIndex in range(len(linesDictionary[line]) - 1):
                currentStop = linesDictionary[line][stopIndex]
                nextStop = linesDictionary[line][stopIndex + 1]
            
            
                tramGraph.add_edge(currentStop, nextStop)
            

        
            g.view_shortest(tramGraph, 'Sandarna', 'Mariaplan', lambda u,v : tramGraph.get_weight(u, v))
        
            
class TramStop:
    def __init__(self, stop, position = None):
        self._stopName = stop
        self._coordinates = position
        self._linesViaStop = []

    def get_stop_name(self):
        return self._stopName

    def get_coordinates(self):
        return self._coordinates
    
    def set_coordinates(self, xCoord, yCoord)
        self._coordinates = tuple(xCoord, yCoord)

    def get_lines_via_stop(self):
        return self._linesViaStop

    def add_line_via_stop(self, line)
        self._linesViaStop.append(line)

class TramLine:
    def __init__(self, line, stops):
        self._lineName = str(line)
        self._stopDictionary = stops

    def get_line_name(self):
        return self._lineName

    def get_stops_in_line(self):
        return self._stopDictionary

class TramNetwork(WeightedGraph):

    def __init__(self, stopDict. lineDict, timeDict):
        super().__init__()
        self._stopDictionary = stopDict
        self._linesDictionary = lineDict
        self._timeDict = timeDict


    def 

    def build_edges_for_tramNetwork(self):

        for line in linesDictionary.keys():
            for stopIndex in range(len(linesDictionary[line]) - 1):
                currentStop = linesDictionary[line][stopIndex]
                nextStop = linesDictionary[line][stopIndex + 1]
                self.add_edge(currentStop, nextStop)
        

    






if __name__ == '__main__':
    main()

