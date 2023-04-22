#!/usr/bin/python3.9

import string
import itertools
import socket
import time
import datetime
import sys
import requests
import os
import sqlite3

pages = 'pages'

if not os.path.isdir(pages):
    os.mkdir(pages)
    print('Created empty %s directory.' % pages)

def dbCreate(fileName):
    con = sqlite3.connect(fileName)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE domains (name text, ip text)
        ''')
    con.commit()
    con.close()
    print("Created empty database.")


dbFileName = 'domains.db'

if not os.path.isfile(dbFileName):
    dbCreate(dbFileName)

con = sqlite3.connect(dbFileName)
cur = con.cursor()
cur.execute('''
    SELECT * FROM domains
    ''')
exist = cur.fetchone()

if exist is None:
    print('"domains" table has no rows...')
    if str(input('Recreate database? [y/N] ')).lower() == 'y':
        os.remove(dbFileName)
        dbCreate(dbFileName)

con.close()


letters = string.ascii_lowercase + string.digits
generation = [''.join(i) for i in itertools.product(letters, repeat=2)]

outputFileName = str(datetime.datetime.now()) + '.log'

for element in generation:
    domainName = element + '.kz'
    try:
        s = socket
        s.setdefaulttimeout(2.0)
        ip = s.gethostbyname(domainName)
        result = " ".join((domainName, ip))
        outputFile = open(outputFileName, 'a')
        con = sqlite3.connect(dbFileName)
        cur = con.cursor()
        cur.execute('''
            INSERT OR IGNORE INTO domains (name, ip) VALUES (?, ?)
            ''', (domainName, ip))
        cur.execute('''
            UPDATE domains
            SET name = ?, ip = ?
            WHERE name = ?
            ''', (domainName, ip, domainName))
        con.commit()
        con.close()
        print(result)
        print(result, file = outputFile)
        outputFile.close()
        schema = 'https'
        try:
            r = requests.get(schema + '://' + domainName, timeout=1)
            print(str(len(r.text)) + ' symbols in HTML')
            with open(pages + '/' + domainName + '.html', 'w') as f:
                f.write(r.text)
            f.close()
        except requests.exceptions.RequestException as e:
            print(e)
    except socket.gaierror as e:
        print(domainName, e)
    time.sleep(3)

