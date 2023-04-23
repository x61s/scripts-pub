#!/bin/python3

import readline
import sqlite3
from sqlite3 import Error

def printHint():
    hints = (
        'l - list top 5 active tasks',
        'la - list all active tasks',
        'lc - list all canceled tasks',
        'a - add new task',
        'e - edit task',
        'c - cancel task',
        'd - delete canceled task from database',
        'da - delete all canceled tasks from database',
        '<number> - show task details',
        'q - quit'
    )
    for hint in hints:
        print(hint)

    print()


def dbLoad(dbName: str):
    # create tasks table
    try:
        print('accessing local database...')
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        query = 'CREATE TABLE tasks(id integer primary key, description text, priority integer default 0, canceled bool default 0, datetime text);'
        cur.execute(query)
        con.close()
    except Error as e:
        print(e)

    # count tasks in db
    try:
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        query = 'SELECT COUNT(*) FROM tasks WHERE canceled = 0;'
        cur.execute(query)
        count = cur.fetchall()[0][0]
        print('You have {0} tasks'.format(count))
        con.close()
    except Error as e:
        print(e)


def listTasks(dbName: str, limit: int, canceled: bool):
    try:
        width = 40
        con = sqlite3.connect(dbName)
        cur = con.cursor()

        query = 'SELECT * FROM tasks WHERE canceled = {0};'.format(canceled)

        if not limit is None:
            query = 'SELECT * FROM tasks WHERE canceled = {0} limit {1};'.format(canceled, limit)

        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            taskNumber = row[0]
            taskDescription = row[1]
            taskPriority = row[2]

            if len(taskDescription) > width:
                taskDescription = row[1][:width] + '...'

            task = '{0}: {1} ({2})'.format(
                taskNumber,
                taskDescription,
                taskPriority)
            print(task)
        con.close()
    except Error as e:
        print(e)


def parseCommand(dbName: str, command: str):
    if command == 'h':
        printHint()
    elif command == 'l':
        listTasks(dbName, 5, canceled = False)
    elif command == 'la':
        listTasks(dbName, None, canceled = False)
    elif command == 'lc':
        listTasks(dbName, None, canceled = True)
    elif command == 'q':
        exit()


def main():
    dbName = 'db.sqlite'
    print('todo v0.1')
    dbLoad(dbName)
    print('h - help')
    while True:
        command = input('> ')
        parseCommand(dbName, command)

if __name__ == '__main__':
    main()
