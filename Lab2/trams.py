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


    with open(TRAM_FILE, 'r') as tramfile:
        tramNet = json.load(tramfile)

        linesDict = tramNet['lines']
        stopsDict = tramNet['stops']
        timesDict = tramNet['times']

        tramGraph = TramNetwork(stopsDict, linesDict, timesDict)


        print(tramGraph.vertices())


        print(tramGraph.edges())

        extreme = tramGraph.extreme_positions()

        print(extreme)


            
        inputt = input()
        if inputt == 't':
            g.view_shortest(tramGraph, 'Sandarna', 'Kungssten', lambda u,v : tramGraph.transition_time(u,v))
        elif inputt == 'd':
            g.view_shortest(tramGraph, 'Sandarna', 'Munkebäckstorget', lambda u,v : tramGraph.geo_distance(u,v))
            
class TramStop:
    def __init__(self, stop, position = None):
        self._stopName = stop
        self._coordinates = position
        self._linesViaStop = []

    def get_stop_name(self):
        return self._stopName

    def get_coordinates(self):
        return self._coordinates
    
    def set_coordinates(self, xCoord, yCoord):
        self._coordinates = tuple(xCoord, yCoord)

    def get_lines_via_stop(self):
        return self._linesViaStop

    def add_line_via_stop(self, line):
        self._linesViaStop.append(line)



class TramLine:
    def __init__(self, line, stops):
        self._lineName = str(line)
        self._stopDictionary = stops

    def get_line_name(self):
        return self._lineName

    def get_stops_in_line(self):
        return self._stopDictionary



class TramNetwork(g.WeightedGraph):

    def __init__(self, stopDict, lineDict, timeDict):
        super().__init__()
        self._stopDictionary = stopDict
        self._linesDictionary = lineDict
        self._timesDictionary = timeDict

        for line in self._linesDictionary.keys():
            for stopIndex in range(len(self._linesDictionary[line]) - 1):
                currentStop = self._linesDictionary[line][stopIndex]
                nextStop = self._linesDictionary[line][stopIndex + 1]
                self.add_edge(currentStop, nextStop)

    def all_lines(self):
        return self._linesDictionary.keys()
    
    def all_stops(self):
        return self._stopDictionary.keys()
    
    def extreme_positions(self):
        maxLat = 0
        minLat = float('inf')
        maxLon = 0
        minLon = float('inf')
        for stop in self._stopDictionary.keys():
            stopLat = float(self._stopDictionary[stop]['lat'])
            stopLon = float(self._stopDictionary[stop]['lon'])
            maxLat = max(maxLat, stopLat)
            minLat = min(minLat, stopLat)
            maxLon = max(maxLon, stopLon)
            minLon = min(minLon, stopLon)
        
        return [maxLat, minLat, maxLon, minLon]

    def geo_distance(self, stop1, stop2):
        distance = td.distance_between_stops(self._stopDictionary, stop1, stop2)
        return distance
    
    def line_stops(self, line):
        return self._linesDictionary[line]
    
    def stop_lines(self, stop):
        linesViaStop = td.lines_via_stop(self._linesDictionary, stop)
        return linesViaStop
        
    def stop_position(self, stop):
        latPosition = self._stopDictionary[stop]['lat']
        lonPosition = self._stopDictionary[stop]['lon']
        return (latPosition, lonPosition)
    
    def transition_time(self, stop1, stop2):
        line = td.lines_between_stops(self._linesDictionary, stop1, stop2)[0]
        print(line)
        time = td.time_between_stops(self._linesDictionary, self._timesDictionary, line, stop1, stop2)
        return time

        
        

    






if __name__ == '__main__':
    main()

