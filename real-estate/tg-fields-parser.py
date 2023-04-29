#!/bin/python3

import json, re


inputFile = open('dedup-output.json', 'r')
exportFile = open('output.json', 'w')

data = json.load(inputFile)

exportDict = {}

for key in data:
    print(key)
    internalDict = {}
    internalDict['Date'] = data[key][0]

    msg = data[key][1]

    internalDict['Rooms'] = '-'
    if '1+1' in msg:
        internalDict['Rooms'] = 2

    if '2+1' in msg:
        internalDict['Rooms'] = 3

    internalDict['Property Size'] = '-'
    internalDict['Price'] = '-'

    if ('м2' in msg or
        'м²' in msg):
        msg = msg.replace('м²', 'м2')
        msg = msg.replace(' м2', 'м2')
        splitMsg = msg.split(' ')

        for item in splitMsg:
            if 'м2' in item:
                area = item.replace('м2', '')

                # 'фактически)\nбрутто:90,нетто-85.\n2' notation problem
                if 'фактически)\nбрутто:90,нетто-85.\n2' in area:
                    area = '90'

                # the 50/60 area problem
                if '/' in area:
                    area = area.split('/', 1)[0] # remove all after `/`

                area = int(''.join(symbol for symbol in area if symbol.isdigit()))

                internalDict['Property Size'] = area

    if ('€' in msg):
        msg = msg.replace('1+1', '')
        msg = msg.replace('2+1', '')
        msg = msg.replace(' €', '€')
        msg = re.sub('(?<=\d)\s(?=\d{3})', '', msg) # remove spaces from 130 000€ notation
        msg = msg.replace('\n', ' ')
        splitMsg = msg.split(' ')

        for item in splitMsg:
            if '€' in item:
                price = item.replace('€', '')
                price = int(''.join(symbol for symbol in price if symbol.isdigit()))
                internalDict['Price'] = price

    print('Size:', internalDict['Property Size'], 'Price:', internalDict['Price'], 'Rooms:', internalDict['Rooms'])

    #internalDict['Message'] = msg
    exportDict[key] = internalDict


print(exportDict)
json.dump(exportDict, exportFile, indent=4, sort_keys=True, ensure_ascii=False)

inputFile.close()
exportFile.close()
