#!/usr/bin/env python3

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
	print("Connect - User: {} PW: {} Host: {}  Port: {} DB: {}".format(user,pwDB,host,port,activeDB))
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

# Close Connection
print("Closing Connection")
try:
	conn.close()
	print("Connection closed")
except mariadb.Error as e:
	print(f"Error closing connection: {e}")
	sys.exit(1)

print("Done Test")



