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

# === Test Creating Sensor Readings Database ===
./test_create_db.py

