#!/bin/python3

import json, re
from math import radians
from sklearn.neighbors import BallTree
import numpy as np

inputFile = open('sb-converter-mercator-output.json', 'r')
exportFile = open('sb-converter-coastline-output.json', 'w')

data = json.load(inputFile)

exportDict = {}

def nearest(p, targets):
    p_rad = [(radians(p[0][0]), radians(p[0][1]))]
    print(p, p_rad)

    targets_rad = np.array([[radians(x[0]), radians(x[1])] for x in targets ])
    tree = BallTree(targets_rad, metric = 'haversine')
    result = tree.query(p_rad)
    target_point = result[1].tolist()[0][0]

    earth_radius = 6371000 # meters in earth
    distance = result[0][0] * earth_radius

    return target_point, round(distance[0])


# nearest cloastline points for each df property object
print('Nearest coastline and highway points for each property object:')

coastFile = open('coastline.json', 'r')
clData = json.load(coastFile)
coastFile.close()

coastline = []

for key in clData:
    coastline.append((clData[key]['Lon'], clData[key]['Lat']))

print(coastline)

highwayFile = open('highway.json', 'r')
hwData = json.load(highwayFile)
highwayFile.close()

highway = []

for key in hwData:
    highway.append((hwData[key]['Lon'], hwData[key]['Lat']))

for key in data:
    print(key)
    print(data[key])
    
    internalDict = {}
    for k, v in data[key].items():
        print(k, v)
        internalDict[k] = v
    
    internalDict['CoastLon'] = ''
    internalDict['CoastLat'] = ''
    internalDict['SeaDistance'] = ''
    internalDict['HighwayLon'] = ''
    internalDict['HighwayLat'] = ''
    internalDict['HighwayDistance'] = ''
    
    try:
        lon = data[key]['Lon']
        lat = data[key]['Lat']
        prop = [(float(data[key]['Lon']), float(data[key]['Lat']))]
        index, clDist = nearest(prop, coastline)
        print('Coast point: {0} Distance: {1}m'.format(coastline[index], clDist))
        
        internalDict['CoastLon'] = coastline[index][0]
        internalDict['CoastLat'] = coastline[index][1]
        internalDict['SeaDistance'] = clDist
        
        index, hwDist = nearest(prop, highway)
        print('Highway point: {0} Distance: {1}m'.format(highway[index], hwDist))
        
        internalDict['HighwayLon'] = highway[index][0]
        internalDict['HighwayLat'] = highway[index][1]
        internalDict['HighwayDistance'] = hwDist

    except Exception as e:
        print(e)
    

    exportDict[key] = internalDict


print(exportDict)
json.dump(exportDict, exportFile, indent=4, sort_keys=True, ensure_ascii=False)

inputFile.close()
exportFile.close()
