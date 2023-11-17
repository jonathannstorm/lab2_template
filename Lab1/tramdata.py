import sys
import json
import math


# files given   
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'

# file to give
TRAM_FILE = './tramnetwork.json'
    



def build_tram_stops(jsonobject):
    dictOfStops = {}
    # translates the JSON file to a python dictionary
    with open(jsonobject) as jsonFile:
        dictOfJsonObjects = json.load(jsonFile)
    
    for (key,value) in dictOfJsonObjects.items():
        # creates a dictionary to store lat and lon values
        dictOfPositions = {}

        # adds the values from JSON object key 'position' as seperate values in a dictionary
        dictOfPositions['lat'] = value['position'][0]
        dictOfPositions['lon'] = value['position'][1]
        
        # adds the dictionary of lat and lon to dictOfStops[stop]
        dictOfStops[key] = dictOfPositions

    return dictOfStops
        


        

def build_tram_lines(lines):
    lineDict = {}  # Skapa en tom dictionary för att lagra linjeinformationen
    listOfStopTimes = []
    
    with open(lines) as file:
        currentLine = 0

        for row in file:

            # row är linjenummer, skapa som nyckel till lineDict
            if row[0].isdigit():
                row = row.rstrip("\n")
                row = row.rstrip(":")
                currentLine = row
                lineDict[currentLine] = []

            # row är tom, strunta i den
            elif row[0] == '\n':
                pass

            
            else:
                listan = row.split()
                
                currentStop = ''

                # manipulera strängen på row så att det endast är stoppet
                for element in listan:
                    if element.startswith('1'):
                        splitTime = element.split(':')
                        stopTime = int(splitTime[1])
                        listOfStopTimes.append(stopTime)
                        break
                    currentStop = (currentStop + ' ' + element).lstrip(' ')
                
                # lägg till currentStop till listan currentLine mappar till i lineDict
                
                lineDict[currentLine].append(currentStop)
            
    timeDict = build_time_dict(lineDict, listOfStopTimes)

    return lineDict, timeDict

        

def build_time_dict(dictionary, list):
    timeDict = {}
    # ändring av namn för förståelsens skull
    notFinishedListOfTimes = list

    # gör varje hållplats till en key (utan value) i timeDict
    for key in dictionary.keys():
        for stop in dictionary[key]:
            timeDict[stop] = {}
    
    # lista för faktiska tider mellan stop
    listOfTimes = []

    # algoritm för att få fram faktiska tider mellan stop
    while len(notFinishedListOfTimes) > 1:
        nextStopTime = int(notFinishedListOfTimes[1])
        thisStopTime = int(notFinishedListOfTimes[0])
        timeBetweenStops = nextStopTime - thisStopTime

        # om vi är kvar på samma spårvagnslinje (blir negativa värden om linje[i]stop[j] - linje[i + 1]stop[0])
        # lägg till faktiska värdet mellan stop [j] och stop [j + 1] i listOfTimes
        # ta bort tiden som använts som nuvarande stop [j]
        if timeBetweenStops >= 0:
            listOfTimes.append(timeBetweenStops)
            notFinishedListOfTimes.pop(0)
        
        # om vi byter spårvagnslinje så läggs aldrig linje[i]stop[j] - linje[i + 1]stop[0] till i listOfTimes
        else:
            notFinishedListOfTimes.pop(0)
            continue

    # algoritm för att iterera över alla hållplatser och matcha dem med sina tider sinsemellan från listOfTimes
    for key in dictionary.keys():
        for stopIndex in range(len(dictionary[key]) - 1):
            # timeDict[stop[i]] uppdateras till att innehålla alla sina sammanhängande hållplatser och tiden
            timeDict[dictionary[key][stopIndex]] = {**timeDict[dictionary[key][stopIndex]], 
                                                    dictionary[key][stopIndex + 1]: listOfTimes.pop(0)
                                                    }
    return timeDict



def build_tram_network(stopfile, linefile):
    tramNetworkDict = {"stops" : {},
                   "lines" : {},
                   "times" : {}
                   }
    
    # skapa alla dictionaries som behövs
    dictionaryOfStops = build_tram_stops(stopfile)
    dictionaryOfLines , dictionaryOfTimes = build_tram_lines(linefile)
    

    tramNetworkDict['stops'] = dictionaryOfStops
    tramNetworkDict['lines'] = dictionaryOfLines
    tramNetworkDict['times'] = dictionaryOfTimes

    with open(TRAM_FILE, 'w') as file:
        json.dump(tramNetworkDict, file, indent=2)

def lines_via_stop(linedict, stop):
    linesViaStop = []

    # iterera över alla linjer, finns stop med läggs linjen till i linesViaStop
    for key in linedict.keys():
        for currentStop in linedict[key]:
            if currentStop == stop:
                linesViaStop.append(key)

    return linesViaStop
    

def lines_between_stops(linedict, stop1, stop2):
    linesBetweenStops = []

    # skapa två lseparata istor innehållandes av linjerna genom stop1 respektive stop2
    linesViaStop1 = lines_via_stop(linedict, stop1)
    linesViaStop2 = lines_via_stop(linedict, stop2)
    
    # Om listan över linjer genom stop2 innehåller samma linje som går genom stop1 = linje mellan stop1 och stop2
    for element in linesViaStop1:
        if linesViaStop2.__contains__(element):
            linesBetweenStops.append(element)

    
    return linesBetweenStops

def time_between_stops(linedict, timedict, line, stop1, stop2):
    
    # skapa en lista med linjerna som går mellan stop1 och stop2
    linesBetweenStops = lines_between_stops(linedict, stop1, stop2)

    # om line inte finns med i linesBetweenStops
    if line not in linesBetweenStops:
        print(f'{line} does not exist between {stop1} and {stop2}')
        return None
    
    # beräkning av två olika tider
    # beror på åt vilket håll en tänkt åka
    time1 = time_between_stop_helper(timedict, linedict[line], stop1, stop2)
    time2 = time_between_stop_helper(timedict, linedict[line], stop2, stop1)

    # ena tiden blir 0 och andra något positivt heltal, ta därför max
    time = max(time1, time2)

    return time

def time_between_stop_helper(timedict, listOfStops, stop1, stop2):
    timeBetweenStops = 0

    # variabel för att bestämma när beräkning av tid ska ske
    countTime = False

    # iterering över alla stop på linjen
    for stopIndex in range(len(listOfStops) - 1):
        
        currentStop = listOfStops[stopIndex]
        nextStop = listOfStops[stopIndex + 1]

        # framme vid start, nu kommer timeBetweenStops börja beräknas
        if currentStop == stop1:
            countTime = True
        
        # framme vid slut, timeBetweenStops slutar beräknas
        if currentStop == stop2:
            countTime = False
            break
        
        # för mellanliggande hållplatser, addera tiderna
        if countTime == True:
            time = timedict[currentStop][nextStop]
            timeBetweenStops += time
    
    return timeBetweenStops
    
def distance_between_stops(stopdict, stop1, stop2):
    # uppskatatd radie av jorden
    R = 6371

    degLat1 = stopdict[stop1]['lat']
    degLon1 = stopdict[stop1]['lon']
    degLat2 = stopdict[stop2]['lat']
    degLon2 = stopdict[stop2]['lon']

    # konvertera latituder och longituder till radianer
    converter = lambda d : float(d) * math.pi / 180
    radLat1 = converter(degLat1)
    radLon1 = converter(degLon1)
    radLat2 = converter(degLat2)
    radLon2 = converter(degLon2)

    # beräkna skillnad mellan latituder och longituder (Δϕ och Δλ)
    deltaPhi = radLat2- radLat1
    deltaLambda = radLon2- radLon1

    # beräkna genomsnittlig latitud ϕm 
    phiM = (radLat1 + radLat2) / 2

    # beräkna haversine
    a = deltaPhi**2
    b = (math.cos(phiM) * deltaLambda) ** 2
    c = math.sqrt(a + b)
    distance = R * c
    
    return distance

def answer_query(tramdict, query):
    queryAsList = query.split(' ', 1)
    
    if queryAsList[0] == 'via':
        linesViaStop = lines_via_stop(tramdict['lines'], queryAsList[1])
        print(f'Lines via {query} is:')
        for element in linesViaStop:
            print(element)
        return linesViaStop

    elif queryAsList[0] == 'between':
        listOfStops = queryAsList[1].split(' and ')

        stop1 = listOfStops[0]
        stop2 = listOfStops[1]
        linesBetweenStops = lines_between_stops(tramdict['lines'], stop1, stop2)
       
        print(f'Lines between {stop1} and {stop2} are:')
        for line in linesBetweenStops:
            print(line)
        return linesBetweenStops

    elif queryAsList[0] == 'time':
        queryListSplit = queryAsList[1].split(' from ', 3)
        
        listWithLine = queryListSplit[0].split()
        line = listWithLine[1]
                
        listOfStops = queryListSplit[1].split(' to ')
        stop1 = listOfStops[0]
        stop2 = listOfStops[1]

        time = time_between_stops(tramdict['lines'], tramdict['times'], line, stop1, stop2)

        if time == None:
            print('unknown arguments')
            return

        print(f'Time between {stop1} and {stop2} is {time} minutes')
        return time
    
    elif queryAsList[0] == 'distance':
        
        queryListSplit1 = queryAsList[1].split('from ')
        listOfStops = queryListSplit1[1].split(' to ')

        stop1 = listOfStops[0]
        stop2 = listOfStops[1]

        distance = distance_between_stops(tramdict['stops'], stop1, stop2)
        distance = round(distance, 3)

        print(f'Distance between {stop1} and {stop2} is {distance} km')
        return distance

    else:
        print('sorry, try again')

def dialogue(tramfile=TRAM_FILE):
    with open(tramfile, 'r') as tramfile:
        tramDict = json.load(tramfile)
        while True:
            query = input('Query > ')
            if query == 'quit':
                break
            answer_query(tramDict, query)

if __name__ == '__main__':

    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue()