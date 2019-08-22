#!/usr/bin/env python3
#
# d1.py   delete any temps below 0
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

conn = sqlite3.connect("carldb.db")
sensor_data_table = "sensor_data"
cur = conn.cursor()

# delete all negative value temps
cur.execute("DELETE FROM " + sensor_data_table + " WHERE payload LIKE '%temp%-%'")
cur.execute("DELETE FROM " + sensor_data_table + " WHERE sensor_value LIKE '-%'")
conn.commit()
print("Deleted all negative temps")

# delete all processed temps
cur.execute("DELETE FROM " + sensor_data_table + " WHERE processed = 1")
conn.commit()
print("Deleted all processed temps")


# print out all rows of sensor_data table
cur.execute("SELECT * FROM sensor_data;")
all_rows = cur.fetchall()
print("\nAll sensor_data:")
for row in all_rows:
    print(row)

conn.close()

