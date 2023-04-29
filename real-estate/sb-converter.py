#!/bin/python3

import json, re


inputFile = open('example-for-sale-20230416-235024.json', 'r')
exportFile = open('example-converted-output.json', 'w')

data = json.load(inputFile)

exportDict = {}
rate = 0.047 # try eur exchange rate
for key in data:
    print(key)
    internalDict = {}
    internalDict['Link'] = data[key][0]
    internalDict['Description'] = data[key][1]
    internalDict['Property Size'] = data[key][2]

    rooms = data[key][3]
    if rooms == 'Studio Flat (1+0)':
        rooms = '1'
    elif rooms == '4.5+1':
        rooms = '5'
    else:
        rooms = sum(int(i) for i in data[key][3].split('+'))

    internalDict['Rooms'] = rooms

    price = int(''.join(symbol for symbol in data[key][4] if symbol.isdigit())) * rate
    internalDict['Price'] = int(price)
    internalDict['Date'] = data[key][5]
    internalDict['Location'] = data[key][6]

    exportDict[key] = internalDict

print(exportDict)
json.dump(exportDict, exportFile, indent=4, sort_keys=True, ensure_ascii=False)

inputFile.close()
exportFile.close()
