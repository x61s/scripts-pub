#!/usr/bin/python3.9

import sys
import requests
import re

def getURLsFrom(targets):
    urls = list()
    for item in targets:
        try:
            r = requests.get(item, timeout=1)
            urls.append(re.findall(r'(https?://[^\s]+)', r.text))
        except requests.exceptions.RequestException as e:
            print(e)
    return urls

def printResults(urls, level):
    count = 0
    for items in urls:
        for url in items:
            print(level)
            print(url)
            count += 1
    print(str(count) + ' URLs found')

def generateNewTargetsFrom(urls):
    target.clear()
    for items in urls:
        for url in items:
            target.append(url)
    return target

print('Parsing URL: %s' % sys.argv[1])

level = 0
target = list()
target.append(sys.argv[1])

urls = getURLsFrom(target)
printResults(urls, level)

level += 1
target = generateNewTargetsFrom(urls)
urls = getURLsFrom(target)
printResults(urls, level)

# while(True):
#     if len(urls) > 0:
#         question = 'Do you want to check this URLs? [Y/n] '
#         answer = str(input(question)).lower() or None
#         if answer == 'y' or answer is None:
#             target.clear()
#             target.append(urls)
#             level += 1
#         else:
#             break
#     printResults(getURLs(target), level)

