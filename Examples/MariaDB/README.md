
# Using MariaDB on Raspbian For Robots

(MariaDB is an open-source fork of MySQL at purchase by Oracle.)

# === FOR MORE INFO on MariaDB ====

https://mariadb.com/docs/appdev/connector-python/

# === To Bring Down To Your GoPiGo  
```
wget https://github.com/slowrunner/Carl/raw/master/Examples/MariaDB/MariaDBdemo.tgz 
tar -xzvf MariaDBdemo.tgz
```

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

# === Add Python3 Interface To MariaDB
pip3 install mariadb


# === List MariaDB users ===
```
./test_list_users.py
test_list_user.py
Executing list_users.sql
Existing Users
User
root

Done
```

# === Create pi user for MariaDB
```
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
```

# === To drop a user from MariaDB
(If you drop pi user, you must create pi user again!)
(DO NOT DROP root USER!)

```
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
```

# === Rename password key file for use ===
```
$ mv mariadb.key.new mariadb.key
```

# === Test Connection to MariaDB for pi user with pw in key file
```
$ ./test_connection.py
Connect - User: pi PW: pipassword Host: 127.0.0.1  Port: 3306 DB: 
Connection successful
Closing Connection
Connection closed
Done Test
```

# === Test Dropping Sensor Readings Database ===
```
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
```

# === Test Creating Sensor Readings Database ===
```
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
```

# === Test Dropping Sensor Readings Table from carldb Database ===
```
./test_table_drop.py 
Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Error connecting to MariaDB carldb: Unknown database 'carldb'
```

# === Test Creating Sensor Readings Table in carldb Database ===
```
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
```

# === Test Adding Data to Table ===
```
$ ./test_data_add.py 

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Connection successful

sensor_name? distance
sensor_reading? 21.2
sensor_units? mm
add the sensor reading
Insert Success
retrieve sensor reading
(1, 'distance', '21.2', 'mm', datetime.datetime(2021, 1, 27, 12, 35, 17))
Commit Change? y
Closing Connection
Connection closed
Done Test
```

NOTE: Suggest add two more records for demonstration:  
- light  120  (0-255)  
- distance 3000 mm  


# === Test Listing Data in carldb.sensor_data ===
```
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
```

# === Test using WHERE to extract only one sensor's reading(s)
```
$ ./test_data_where.py 

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Connection successful

First Listing All Rows
1 - distance: 21.2 mm at 21-01-27 12:35:17
2 - light: 120 0-255 at 21-01-27 12:43:51

Now Only Readings For One Type Of Sensor

sensor_name? distance

Retrieve distance sensor reading(s)
Query:  
	SELECT sensor_name, sensor_value, sensor_units, sensor_dt
	FROM sensor_data
	WHERE sensor_name=?
	 ('distance',)
Returns Rows:
('distance', '21.2', 'mm', datetime.datetime(2021, 1, 27, 12, 35, 17))

Retrieve sensor readings not using fetchall()
distance 21.2 mm at 2021-01-27 12:35:17

Closing Connection
Connection closed
Done Test
```

# === Test Update Latest Record Of A Sensor ===  

Example changing last distance reading from 3000 mm to 200 mm:  

```
$ ./test_update_last.py 

Executing test_update_last.py

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Connection successful

Retrieve sensor readings
(1, 'distance', '21.2', 'mm', datetime.datetime(2021, 1, 27, 12, 35, 17))
(2, 'light', '120', '0-255', datetime.datetime(2021, 1, 27, 12, 43, 51))
(3, 'distance', '3000', 'mm', datetime.datetime(2021, 1, 28, 7, 31, 48))

Reading To Update
sensor_name? distance
New sensor_reading? 200
New sensor_units? mm
Updating the sensor reading and units
Update Attempted

Retrieve sensor readings
(1, 'distance', '21.2', 'mm', datetime.datetime(2021, 1, 27, 12, 35, 17))
(2, 'light', '120', '0-255', datetime.datetime(2021, 1, 27, 12, 43, 51))
(3, 'distance', '200', 'mm', datetime.datetime(2021, 1, 28, 7, 42, 12))

Commit Change? y
Closing Connection
Connection closed
Done Test
```

# === Test Dropping Specific Row ====  
```
$ ./test_row_drop.py

Executing test_update_last.py

Connect - User: pi PW: **** Host: 127.0.0.1  Port: 3306 DB: carldb
Connection successful

Retrieve sensor readings
(1, 'distance', '21.2', 'mm', datetime.datetime(2021, 1, 27, 12, 35, 17))
(2, 'light', '124', '(0-255)', datetime.datetime(2021, 1, 28, 7, 42, 51))
(3, 'distance', '200', 'mm', datetime.datetime(2021, 1, 28, 7, 42, 12))

Row To Drop
id? 1
Dropping row 1
Executing Query: 
	DELETE FROM carldb.sensor_data
	WHERE id=?
	
Drop Attempted

Retrieve sensor readings
(2, 'light', '124', '(0-255)', datetime.datetime(2021, 1, 28, 7, 42, 51))
(3, 'distance', '200', 'mm', datetime.datetime(2021, 1, 28, 7, 42, 12))

Commit Change? y
Closing Connection
Connection closed
Done Test
```

# === TO STOP MARIADB FROM STARTING AT BOOT ====  
```
$ sudo systemctl stop mariadb
$ sudo systemctl disable  mariadb
Removed /etc/systemd/system/multi-user.target.wants/mariadb.service.
Removed /etc/systemd/system/mysqld.service.
Removed /etc/systemd/system/mysql.service.
$ sudo systemctl stop mysql
$ sudo systemctl disable mysql

NOTE: to see it is still there

$ systemctl list-unit-files | grep mariadb
mariadb.service                        disabled       
mariadb@.service                       disabled 
$ systemctl list-unit-files | grep mysql
mysql.service		generated      
```

# === TO RE-ENABLE MARIADB TO START AT BOOT ===  
```
$ sudo systemctl enable mariadb  
$ sudo systemctl start mariadb  
$ sudo systemctl enable mysql
$ sudo systemctl start mysql
```
