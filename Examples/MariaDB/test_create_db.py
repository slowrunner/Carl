#!/usr/bin/env python3

# FILE: test_create_db.py

import mariadb
import sys
import os
import traceback

user="pi"
host="127.0.0.1"
port=3306
activeDB=""

def getDBpw():
	with open('mariadb.key', 'r') as keyfile:
		key = keyfile.readline()
		key = key.rstrip(os.linesep) # remove EOL
	return key

# Get DB Password from mariadb.key file
try:
	pwDB = getDBpw()
	print("\nConnect - User: {} PW: {} Host: {}  Port: {} DB: {}".format(user,pwDB,host,port,activeDB))
except Exception as e:
	print("Exception Getting DB Password, check path and file mariadb.key")
	print(str(e))
	traceback.print_exc()
	sys.exit(1)

# Connect to MariaDB Platform
try:
	conn = mariadb.connect(
		user=user,
		password=pwDB,
		host=host,
		port=port,
		database=activeDB
	)
	print("Connection successful")
except mariadb.Error as e:
	print(f"Error connecting to MariaDB: {e}")
	sys.exit(1)

# Get a cursor object
cur = conn.cursor()

# Create a database
try:
	print("\nCreating DB carldb")
	cur.execute("CREATE DATABASE carldb")
except mariadb.Error as e:
	print(f"Error creating DB carldb: {e}")


# List Databases
print("\nListing Databases")
cur.execute("SHOW DATABASES")
databaseList = cur.fetchall()
for db in databaseList:
	print(db)


# Close Connection
print("\nClosing Connection")
try:
	conn.close()
	print("Connection closed")
except mariadb.Error as e:
	print(f"Error closing connection: {e}")
	sys.exit(1)

print("Done Test")



