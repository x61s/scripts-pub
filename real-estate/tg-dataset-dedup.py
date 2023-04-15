#!/bin/python3

import json

inputFile = open('input.json', 'r')
exportFile = open('dedup-output.json', 'w')

data = json.load(inputFile)

# removing duplicates

duplicates = []
uniqueDict = {}
duplicatesCount = 0
totalCount = 0

for key, value in data.items():
    totalCount += 1
    print(value[1])
    if value[1] not in duplicates:
        duplicates.append(value[1])
        uniqueDict[key] = value
    else:
        duplicatesCount += 1

print('Total messages:', totalCount)
print('Duplicate messages removed:', duplicatesCount)

json.dump(uniqueDict, exportFile, indent=4, sort_keys=True, ensure_ascii=False)

inputFile.close()
exportFile.close()
