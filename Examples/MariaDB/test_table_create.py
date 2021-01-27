#!/usr/bin/env python3

# FILE: test_table_create.py

"""
    assumes test_connection.py success
    assumes test_db_create.py success
"""

import mariadb
import sys
import os
import traceback

user="pi"
host="127.0.0.1"
port=3306
activeDB="carldb"

def getDBpw():
	with open('mariadb.key', 'r') as keyfile:
		key = keyfile.readline()
		key = key.rstrip(os.linesep) # remove EOL
	return key

def create_connection(host_name, user_name, tgt_db):

	# Get DB Password from mariadb.key file
	try:
		pwDB = getDBpw()
		print("\nConnect - User: {} PW: {} Host: {}  Port: {} DB: {}".format(user_name,"****",host_name,port,tgt_db))
	except Exception as e:
		print("Exception Getting DB Password, check path and file mariadb.key")
		print(str(e))
		traceback.print_exc()
		sys.exit(1)

	# Connect to MariaDB Platform
	try:
		conn = mariadb.connect(
			user=user_name,
			password=pwDB,
			host=host_name,
			port=port,
			database=tgt_db
		)
		print("Connection successful")
		return conn
	except mariadb.Error as e:
		print(f"Error connecting to MariaDB {tgtDB}: {e}")
		sys.exit(1)

def execute_query(cur, q):
	try:
		print("Query: ",q)
		cur.execute(q)
		print("Query Success")
	except mariadb.Error as e:
		print(f"Error: {e}")


def main():
	conn = create_connection(host_name=host, user_name=user, tgt_db = activeDB)
	cur = conn.cursor()

	# Create sensor table
	print("\nCreating sensor_data table")
	query="""
	CREATE TABLE IF NOT EXISTS sensor_data (
	id INT PRIMARY KEY AUTO_INCREMENT,
	sensor_name VARCHAR(25),
	sensor_value VARCHAR(10),
	sensor_units VARCHAR(15)
	) ENGINE=InnoDB;
	"""
	execute_query(cur,query)

	# List tables
	print("\nListing Tables")
	cur.execute("SHOW TABLES")
	for (table,) in cur.fetchall():
		print(table)

	# Commit Table
	# conn.commit()

	# Close Connection
	print("\nClosing Connection")
	try:
		conn.close()
		print("Connection closed")
	except mariadb.Error as e:
		print(f"Error closing connection: {e}")
		sys.exit(1)

	print("Done Test")


if __name__ == '__main__': main()

