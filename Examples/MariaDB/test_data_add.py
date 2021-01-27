#!/usr/bin/env python3

# FILE: test_sensor_example.py

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

def add_reading(cur,sensor,value,units):
	q="""
	INSERT INTO carldb.sensor_data 
	(sensor_name,sensor_value,sensor_units)
	VALUES
	(?, ?, ?)
	"""
	try:
		str_value=str(value)
		cur.execute(q,(sensor,str_value,units))
	except mariadb.Error as e:
		print(f"Error: {e}")

def execute_read_query(cur, q):
	try:
		print("Query: ",q)
		cur.execute(q)
		result = cur.fetchall()
		return result
	except mariadb.Error as e:
		print(f"Error: {e}")


def main():
	conn = create_connection(host_name=host, user_name=user, tgt_db = activeDB)
	cur = conn.cursor()

	# Get a reading
	sensor_name=input("\nsensor_name? ")
	sensor_reading=input("sensor_reading? ")
	sensor_units=input("sensor_units? ")

	# Insert some data
	print("add the sensor reading")
	add_reading(cur,sensor_name, sensor_reading, sensor_units);
	print("Insert Success")


	print("retrieve sensor reading")
	query = """
	SELECT * FROM sensor_data
	"""
	rows = execute_read_query(cur,query)

	for r in rows:
		print(r)

	yn=input("Commit Change? ")
	if "y" in yn:
		conn.commit()

	# Close Connection
	print("Closing Connection")
	try:
		conn.close()
		print("Connection closed")
	except mariadb.Error as e:
		print(f"Error closing connection: {e}")
		sys.exit(1)

	print("Done Test")


if __name__ == '__main__': main()

