#!/bin/python3

import requests
from bs4 import BeautifulSoup
import json
from datetime import date


pages = []
page = 0

while True:
    print('Loading page', page)
    url = 'https://www.rixoshome.com.tr/en/search-results/page/'
    url += str(page)
    url += '/?keyword&location%5B0%5D=alanya&areas%5B0%5D=avsallar&status%5B0%5D=for-sale&type%5B0%5D=apartment&rooms&bedrooms&bathrooms&property_id'
    response = requests.get(url)
    if '0 Result Found' in response.text:
        break
    else:
        pages.append(response.text)
        page += 1

print('All pages loaded.')

print('Extracting data...')

urls = set()

for page in pages:
    soup = BeautifulSoup(page, 'html.parser')
    for item in soup.findAll(class_=['btn btn-primary btn-item'], href=True):
        print(item['href'])
        urls.add(item['href'])

apartments = {}
name = 0

for url in urls:
    print()
    print('Loading', url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for section in soup.findAll(class_=['property-detail-wrap property-section-wrap']):
        ul = section.find('ul')
        parameters = {}
        for li in ul.findAll('li'):
            param = li.text.replace('\n','')
            param = param.replace('²','')
            param = param.split(':', 1)

            if param[0] not in ['Property ID', 'Property Type', 'Property Status']:
                param[1] = int(''.join(symbol for symbol in param[1] if symbol.isdigit()))

            parameters[param[0]] = param[1]

        apartments[name] = parameters
        print(name, parameters)
        name += 1

print(apartments)

dt = date.today().strftime("%Y-%m-%d")
filename = 'for-sale-' + dt + '.json'

print('Saving apartments dictionary to', filename)

with open(filename, 'w') as f:
    json.dump(apartments, f, indent=4, sort_keys=True)

