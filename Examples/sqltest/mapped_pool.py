#!/usr/bin/env python3

# mapped_pool.py

# creates a pool of <3> worker processes to take values from a list
# and store them to a lock protected database

# based on https://gist.github.com/filipkral/c51c6a78432706695f176dce0d2ac47a

# RESULTS
#
#  Insert:  Max 43 ms Ave 18ms each for 100 values
#  Insert:  Max 6-11s  Ave 43-105ms for 1000 values

import sqlite3
from contextlib import closing
import multiprocessing
import os
import datetime as dt

ROWS = 1000
WORKERS = 3


def prepare_db(db, tbl, col):
    sql = "CREATE TABLE {0} (id INTEGER primary key, {1} text, pid integer, dtNow timestamp);".format(tbl, col)
    with closing(sqlite3.connect(db)) as cnn:
        cursor = cnn.cursor()
        cursor.execute('DROP TABLE IF EXISTS {0};'.format(tbl))
        cursor.execute(sql)
        cnn.commit()
    return db, tbl, col

def write(db, tbl, col, value, pid):

    # have to set the timeout reasonably high, otherwise "database is locked"
    timeout = 20.0

    with closing(sqlite3.connect(db, timeout=timeout)) as cnn:
        cursor = cnn.cursor()
        dtNow = dt.datetime.now()
        cursor.execute("INSERT INTO {0} ({1}, pid, dtNow) VALUES ('{2}','{3}','{4}');".format(tbl, col, value, pid, dtNow))
        cnn.commit()

def work(d):
    db = r'mapped_pool.db'
    tbl = 'logging'
    col = 'logged'
    pid = os.getpid()

    write(db, tbl, col, d, pid)

    return d

def main():
    data = list(range(ROWS))

    db = r'mapped_pool.db'
    tbl = 'logging'
    col = 'logged'

    prepare_db(db, tbl, col)

    pool = multiprocessing.Pool(WORKERS)
    dtStart = dt.datetime.now()
    mapped = pool.map(work, data)
    dtEnd = dt.datetime.now()
    totalTime = (dtEnd-dtStart).total_seconds()
    aveInsert = totalTime / ROWS
    print("Total Time: {} for {} inserts, {} average".format(totalTime, ROWS, aveInsert))
    pool.close()
    pool.join()

    return mapped

if __name__ == "__main__":
    main()
