import sys
sys.path.append("Lab1")
from Lab1.tramdata import*
from Lab1.data import *

TRAM_LINES = './Lab1/data/tramlines.txt'
TRAM_STOPS = './Lab1/data/tramstops.json'

tramNet = build_tram_network(TRAM_STOPS, TRAM_LINES)

print(tramNet)

