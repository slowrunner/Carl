#!/usr/bin/env python3


import sqlite3
import multiprocessing
import datetime as dt
import time
import os

'''
This program starts a daemon process that listens on a queue.
It then starts <3> processes that place <20K> integers (and pid) each in the queue.
The listening daemon pulls the integer and pid out of the queue and
stores them in the database with a primary key row id, and timestamp.

At the end of all inserts, the number of inserts is printed,
then the first tenth of the total rows of the DB are printed.

RESULTS:  insert to db: 200-750 us average, 2-27 ms max  (6K-60K row db)
          add_to_queue: 86-95 us
          fetch 1 row : 900 us
          fetch all   : 10-15 us per row (600-900 ms total for 60000)

based on https://gist.github.com/cessor/f8bf530212fbe75263c79564f5fc15ad
'''
DB_FILENAME = 'multiproc.db'
INSERTERS = 3
INSERTS = 20000
WAIT4IT = 2

class DbCommands(object):
    CLEAR = 'delete from test'
    DROP = 'drop table if exists test'
    COUNT = 'select count(*) from test'
    INIT = 'create table if not exists test (id integer primary key, value integer not null, dt_value timestamp, pid integer default 0)'
    INSERT = 'insert into test (value, pid, dt_value) values (?, ?, ?)'
    FETCHALL = 'select * from test'
    FETCHONE = 'select * from test where id = 1500'

class Database(object):

    def __init__(self, path):
        self._path = path
        self._connection = None

    def __enter__(self):
        self._connection = sqlite3.connect(self._path)
        # Reset Database
        self.execute(DbCommands.DROP)
        self.execute(DbCommands.INIT)
        self.execute(DbCommands.CLEAR)
        return self

    def __exit__(self, *args, **kwargs):
        self._connection.commit()

    def commit(self):
        self._connection.commit()

    def execute(self, sql, *args):
        cursor = self._connection.cursor()
        if not args:
            return cursor.execute(sql)
        return cursor.execute(sql, args)


class Command(object):

    def __init__(self, *args):
        self._args = args


class Count(Command):

    def execute(self, database):
        count = database.execute(DbCommands.COUNT).fetchall()
        count = count[0][0]
        print('Count: ', count)


class Commit(Command):

    def execute(self, database):
        database.commit()
        raise Break()


class Insert(Command):

    def execute(self, database):
        dtNow = dt.datetime.now()
        database.execute(DbCommands.INSERT, *self._args, dtNow)

class FetchAll(Command):

    def execute(self, database):
       dtNow = dt.datetime.now()
       print("FetchAll started {}".format(dtNow))
       result = database.execute(DbCommands.FETCHALL).fetchall()
       dtNow = dt.datetime.now()
       print("FetchAll complete {}".format(dtNow))
       for i in range(INSERTS//10):
           print(result[i])
       # for row in result:
       #   print(row)

class FetchOne(Command):

    def execute(self, database):
       print("FetchOne Start:",dt.datetime.now())
       result = database.execute(DbCommands.FETCHONE).fetchone()
       print("FetchOne End:",dt.datetime.now())
       print("One Row")
       print(result)

class Break(Exception):
    pass


def handle(queue):
    with Database(DB_FILENAME) as database:
        while True:
            try:
                command = queue.get()
                command.execute(database)
                queue.task_done()

            except Break:
                queue.task_done()
                break

            except Exception as e:
                print(e)


def add_to_queue(queue):
    pid = os.getpid()
    dtNow = dt.datetime.now()
    print("add_to_queue process {} started {}".format(pid,dtNow))
    for i in range(INSERTS):
        queue.put(Insert(i,pid))
    dtNow = dt.datetime.now()
    print("add_to_queue process {} finished {}".format(pid, dtNow))


def main():
    queue = multiprocessing.JoinableQueue()

    # Start a DB writing (daemon) Process
    multiprocessing.Process(target=handle, args=(queue,), daemon=True).start()

    # Start data source Processes
    processes = [
        multiprocessing.Process(target=add_to_queue, args=(queue,))
        for _ in range(INSERTERS)   # 3 requesters
    ]

    # Start Data sources
    for process in processes:
        process.start()

    # Wait until Data sources are done
    for process in processes:
        process.join()

    # Query a command to the database
    queue.put(Count())

    queue.put(FetchAll())
    time.sleep(WAIT4IT)
    print("PutInQueue:",dt.datetime.now())
    queue.put(FetchOne())
    print("AfterPutInQueue:",dt.datetime.now())

    # Send a command to the handler
    # To commit, clean, and close the database
    queue.put(Commit())

    # Do Not Join Daemon Threads,
    # Join their Queues instead
    queue.join()


if __name__ == '__main__':
    main()
