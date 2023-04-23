#!/bin/python3

import readline
import sqlite3
from sqlite3 import Error
from datetime import datetime

class Task:
    taskId = int()
    objective = str()
    priority = int()
    canceled = bool()
    done = bool()
    dt = str()

    def __init__(self, objective = None, priority = None):
        self.objective = objective
        self.priority = priority
        self.canceled = False
        self.done = False
        self.dt = None

    def loadById(self, dbName, taskId: int):
        self.taskId = taskId
        con = sqlite3.connect(dbName)
        cur = con.cursor()

        query = '''
        SELECT * FROM tasks
        WHERE id = {0};
        '''.format(taskId)

        cur.execute(query)
        rows = cur.fetchall()
        con.close()
        if len(rows):
            self.objective = rows[0][1]
            self.priority = rows[0][2]
            self.canceled = rows[0][3]
            self.done = rows[0][4]
            self.dt = rows[0][5]
            return True
        else:
            print('Task not found.')
            return False

    def cancel(self, dbName):
        if not self.taskId is None:
            con = sqlite3.connect(dbName)
            cur = con.cursor()

            query = '''
            UPDATE tasks
            SET canceled = {0}
            WHERE id = {1}
            '''.format(not self.canceled, self.taskId)

            cur.execute(query)
            con.commit()
            con.close()
            self.loadById(dbName, self.taskId)

    def insert(self, dbName):
        try:
            self.dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            con = sqlite3.connect(dbName)
            cur = con.cursor()

            query = '''
            INSERT INTO tasks
            ( objective, priority, canceled, done, datetime )
            VALUES (?, ?, ?, ?, ?);
            '''

            cur.execute(query, (self.objective, self.priority, self.canceled, self.done, self.dt))
            self.taskId = cur.lastrowid
            print(self.taskId)
            con.commit()
            con.close()
        except Error as e:
            print(e)


def dbLoad(dbName: str):
    # create tasks table
    try:
        print('accessing local database...')
        con = sqlite3.connect(dbName)
        cur = con.cursor()

        query = '''
        CREATE TABLE tasks
        ( id integer primary key,
        objective text,
        priority integer default 0,
        canceled bool default 0,
        done bool default 0,
        datetime text );
        '''

        cur.execute(query)
        con.close()
    except Error as e:
        print(e)

    # count tasks in db
    try:
        con = sqlite3.connect(dbName)
        cur = con.cursor()

        query = '''
        SELECT COUNT(*) FROM tasks
        WHERE canceled = 0 AND done = 0;
        '''

        cur.execute(query)
        count = cur.fetchall()[0][0]
        print('You have {0} undone tasks'.format(count))
        con.close()
    except Error as e:
        print(e)


def listTasks(dbName: str, limit: int, canceled: bool, done = False):
    try:
        width = 40
        con = sqlite3.connect(dbName)
        cur = con.cursor()

        query = '''
        SELECT * FROM tasks
        WHERE canceled = {0} AND done = {1};
        '''.format(canceled, done)

        if not limit is None:
            query = '''
            SELECT * FROM tasks
            WHERE canceled = {0} limit {1};
            '''.format(canceled, limit)

        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            taskNumber = row[0]
            taskDescription = row[1]
            taskPriority = row[2]

            if len(taskDescription) > width:
                taskDescription = row[1][:width] + '...'

            task = '{0}. {1} (priority: {2})'.format(
                taskNumber,
                taskDescription,
                taskPriority)
            print(task)
        con.close()
    except Error as e:
        print(e)


def addTask(dbName):
    objective = input('Task: ')
    if not len(objective):
        print('Error: Task required!')
        return None
    priority = input('Priority (default 0): ') or 0
    t = Task(objective, priority)
    print(t, '{0} ({1})'.format(t.objective, t.priority))
    t.insert(dbName)

def cancelTask(dbName):
    taskId = input('Task ID: ')
    if not len(taskId):
        print('Error: Task ID required!')
        return None
    t = Task()
    if t.loadById(dbName, taskId):
        #print(t, '{0} ({1})'.format(t.objective, t.priority))
        t.cancel(dbName)


def printHint():
    hints = (
        'l - list top 5 active tasks',
        'la - list all active tasks',
        'lc - list all canceled tasks',
        'ld - list all done tasks',
        'a - add new task',
        'e - edit task',
        'c - cancel task',
        'd - mark task as done',
        'r - remove canceled task from database',
        'ra - remove all canceled tasks from database',
        '<number> - select task and show details',
        'q - quit'
    )
    for hint in hints:
        print(hint)

    print()


def parseCommand(dbName: str, command: str):
    if command == 'h':
        printHint()
    elif command == 'l':
        listTasks(dbName, 5, canceled = False)
    elif command == 'la':
        listTasks(dbName, None, canceled = False)
    elif command == 'lc':
        listTasks(dbName, None, canceled = True)
    elif command == 'ld':
        listTasks(dbName, None, canceled = False, done = True)
    elif command == 'a':
        addTask(dbName)
    elif command == 'c':
        cancelTask(dbName)
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
