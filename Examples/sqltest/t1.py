#!/usr/bin/env python3
#
# t1.py   Insert new random temp into carldb.db
#                           print all rows
#                           print last row
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
import datetime as dt

conn = sqlite3.connect("carldb.db")
sensor_data_table = "sensor_data"
cur = conn.cursor()

# insert a new random temp into db
temp_value = random.randint(-10,120)
test_data = {"temp":temp_value}
sensor_type = 'json'
# cur.execute("INSERT INTO " + sensor_data_table + " (payload,sensor_type) VALUES (?,?)",  (str(test_data), sensor_type))
cur.execute("INSERT INTO " + sensor_data_table + " (payload,sensor_type) VALUES (?, ?)",  ( str(test_data), sensor_type) )
conn.commit()
print("Inserted {} payload: {} into db".format(sensor_type, test_data))

# insert a new random temp into db
temp_value = random.randint(-10,120)
sensor_type = "temp"
sensor_value = temp_value
dt_event = dt.datetime.now()
cur.execute("INSERT INTO " + sensor_data_table +
    " (sensor_type, sensor_value, dt_event)  VALUES (?, ?, ?)",
      (sensor_type, str(sensor_value), dt_event))
conn.commit()
print("Inserted sensor {} value {} at {} into db".format(sensor_type, sensor_value, dt_event))


# print out all rows of sensor_data table
cur.execute("SELECT * FROM sensor_data;")
all_rows = cur.fetchall()
print("\nAll sensor_data:")
for row in all_rows:
    print(row)


# print last row of sensor_data table
cur.execute("SELECT payload, processed, sensor_type, sensor_value, dt_event  FROM " + sensor_data_table + " ORDER BY id DESC LIMIT 1")
payload, processed, type, value, at = cur.fetchone()
print("\nLast Row payload: {} processed: {} type: {} value: {} at {}".format(payload, processed, type, value, at))

conn.close()

# payloads = []
# for row in rows:
#     payloads.append(json.loads(rows[0].replace("'",'"')))

# print("Last sensor_data row:\n",payloads)
# conn.close()
# exit()
