#!/usr/bin/env python3
#
# mkdb.py    Safely creates carldb.db
#               with table sensor_data
#                  with columns id, payload, processed
#
# based on https://rosietheredrobot.com/2019/08/gold-filling.html
#
# Assumtions:
#     sqlite3 installed (sudo apt-get install sqlite3
#


import sqlite3

conn = sqlite3.connect("carldb.db")  # creates the db
sensor_data_table = "sensor_data"
cur = conn.cursor()
try:
    cur.execute("CREATE TABLE " + sensor_data_table +
          "(id INTEGER PRIMARY KEY, " +
          "payload TEXT DEFAULT NULL, processed INTEGER DEFAULT 0, " +
          "sensor_type TEXT DEFAULT NULL, sensor_value TEXT DEFAULT NULL, " +
          "dt_event timestamp)" )
    conn.commit()

except sqlite3.DatabaseError as e:
    print("Exception: {}".format(e))

conn.close()


