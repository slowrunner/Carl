#!/usr/bin/env python3
#
# u1.py   mark all temps processed 
#                           print all rows
#
# based on https://rosietheredrobot.com/2019/08/gold-filling.html
#
# Assumtions:
#     sqlite3 installed (sudo apt-get install sqlite3
#     db created (sqlite3 carldb.db)
#     sensor_data table created (CREATE TABLE sensor_data (id INTEGER PRIMARY KEY, payload TEXT, processed INTEGER DEFAULT 0);
#     (to quit sqlite3  .exit )
#


import sqlite3
import json
import random

conn = sqlite3.connect("carldb.db")
sensor_data_table = "sensor_data"
cur = conn.cursor()

# insert a new random temp into db
cur.execute("UPDATE " + sensor_data_table + " SET processed = 1 WHERE processed = 0")
conn.commit()
print("Marked all unprocessed rows as processed")


# print out all rows of sensor_data table
cur.execute("SELECT * FROM sensor_data;")
all_rows = cur.fetchall()
print("\nAll sensor_data:")
for row in all_rows:
    print(row)

conn.close()

