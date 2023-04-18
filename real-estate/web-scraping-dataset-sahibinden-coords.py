#!/bin/python3

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.chrome.options import Options 
import time
import undetected_chromedriver as uc

options = uc.ChromeOptions() 
options.headless = False
options.add_argument('--force-dark-mode')
driver = uc.Chrome(use_subprocess=True, options=options) 

driver.maximize_window() 
driver.get('https://www.sahibinden.com')
time.sleep(20)

driver.find_element('xpath', '//*[@id="btn-continue"]').click()
time.sleep(20)

driver.find_element('xpath', '//*[@id="onetrust-accept-btn-handler"]').click()
time.sleep(5)

pages = []

for offset in range(0, 500, 50):
    print('Current offset', offset)
    url = 'https://www.sahibinden.com/en/for-sale-flat/antalya-alanya-alanya-avsallar?'
    url += 'pagingOffset=' + str(offset)
    url += '&pagingSize=50'
    url += '&sorting=date_desc'
    print('Processing URL', url)
    driver.get(url)
    pages.append(driver.page_source)
    time.sleep(5)

print('All pages loaded.')

from bs4 import BeautifulSoup

print('Extracting data...')

apartments = {}
counter = 0

for page in pages:
    soup = BeautifulSoup(page, 'html.parser')
    for item in soup.findAll('tr', class_=['searchResultsItem']):
        cell_data = []
        for link in item.findAll(class_=['classifiedTitle'], href=True):
            cell_data.append(link['href'])

            url = 'https://www.sahibinden.com'
            url += link['href']
            driver.get(url)
            lat = ''
            lon = ''
            try:
                driver.find_element('xpath', '//*[@id="map"]').click()
                time.sleep(5)
                details = BeautifulSoup(driver.page_source, 'html.parser')
                gmap = details.find('div', {'id': 'gmap'})
                lat = gmap['data-lat']
                lon = gmap['data-lon']
            except:
                pass
            print(lat, lon)
            cell_data.append(lat)
            cell_data.append(lon)
            time.sleep(5)

        for cell in item.findAll('td'):
            text = cell.text.replace('\n', '').strip()
            if len(text):
                cell_data.append(text)
        if len(cell_data):
            apartments[counter] = cell_data
            counter += 1

print(apartments)

driver.close()

import json

dt = time.strftime("%Y%m%d-%H%M%S")
filename = 'sahibinden-for-sale-' + dt + '.json'

print('Saving apartments dictionary to', filename)

with open(filename, 'w') as f:
    json.dump(apartments, f, indent=4, sort_keys=True, ensure_ascii=False)
