# Using MariaDB on Raspbian For Robots

(MariaDB is an open-source fork of MySQL at purchase by Oracle.)

# === Check MariaDB is Running ===
```
$ systemctl status mariadb
```

# === Show who is using MariaDB ===
```
$ sudo mysql -u root -e 'show processlist'
```
- InnoDB is the storage engine for the MySQL / MariaDB dbms (data base management system.  
  (provides ACID-compliant transaction features along with foreign key support).

# === List MariaDB users ===
./test_list_users.py
test_list_user.py
Executing list_users.sql
Existing Users
User
root

Done


# === Create pi user for MariaDB
./test_add_user.py
test_add_user.py
User to add: pi
Password for pi: pipassword
Create user: pi with pw: pipassword? y
Executing add_user.sql
Existing Users
User
root

Create User

User
pi
root

Grants for pi@localhost
GRANT ALL PRIVILEGES ON *.* TO `pi`@`localhost` IDENTIFIED BY PASSWORD '*123456'
Done
Writing pw into mariadb.key.new
Rename without .new to use it

Done

# === To drop a user from MariaDB
$ ./test_drop_user.py 
test_drop_user.py
User to drop: pi
Drop user: pi? y
Executing drop_user.sql
Existing Users
User
pi
root
 
Droping User If Exists
 
User List Now
User
root
 
Done

# === Rename password key file for use ===
$ mv mariadb.key.new mariadb.key

# === Test Connection to MariaDB for pi user with pw in key file
$ ./test_connection.py
Connect - User: pi PW: pipassword Host: 127.0.0.1  Port: 3306 DB: 
Connection successful
Closing Connection
Connection closed
Done Test

# === Test Dropping Sensor Readings Database ===
$ ./test_drop_db.py 

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: 
Connection successful

Listing Databases
('information_schema',)
('mysql',)
('performance_schema',)

Dropping DB carldb
Error dropping DB carldb: Can't drop database 'carldb'; database doesn't exist

Listing Databases
('information_schema',)
('mysql',)
('performance_schema',)

Closing Connection
Connection closed
Done Test


# === Test Creating Sensor Readings Database ===
$ ./test_create_db.py 

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: 
Connection successful

Creating DB carldb

Listing Databases
('carldb',)
('information_schema',)
('mysql',)
('performance_schema',)

Closing Connection
Connection closed
Done Test

# === Test Dropping Sensor Readings Table from carldb Database ===
./test_table_drop.py 
Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Error connecting to MariaDB carldb: Unknown database 'carldb'

# === Test Creating Sensor Readings Table in carldb Database ===
$ ./test_table_create.py 

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Connection successful

Creating sensor_data table
Query:  
	CREATE TABLE IF NOT EXISTS sensor_data (
	id INT PRIMARY KEY AUTO_INCREMENT,
	sensor_name VARCHAR(25),
	sensor_value VARCHAR(10),
	sensor_units VARCHAR(15),
	sensor_dt TIMESTAMP
	) ENGINE=InnoDB;
	
Query Success

Listing Tables
sensor_data

Closing Connection
Connection closed
Done Test

# === Test Adding Data to Table ===
$ ./test_data_add.py 

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Connection successful

sensor_name? distance
sensor_reading? 21.2
sensor_units? mm
add the sensor reading
Insert Success
retrieve sensor reading
Query:  
	SELECT * FROM sensor_data
	
(1, 'distance', '21.2', 'mm', datetime.datetime(2021, 1, 27, 12, 35, 17))
Commit Change? y
Closing Connection
Connection closed
Done Test

# === Test Listing Data in carldb.sensor_data ===

$ ./test_data_list.py 

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Connection successful

Retrieve sensor reading
Query:  
	SELECT * FROM sensor_data
	
(1, 'distance', '21.2', 'mm', datetime.datetime(2021, 1, 27, 12, 35, 17))
Closing Connection
Connection closed
Done Test

