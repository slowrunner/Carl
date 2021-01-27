\! echo "Executing add_user.sql";
use mysql;
\! echo "Existing Users"
SELECT User FROM mysql.user;
\! echo "";
\! echo "Create User"
CREATE USER IF NOT EXISTS 'newuser'@localhost IDENTIFIED by 'newpw';
\! echo "";
SELECT User FROM mysql.user;
\! echo "";
GRANT ALL PRIVILEGES ON *.* To 'newuser'@localhost IDENTIFIED BY 'newpw';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'newuser'@localhost;
\! echo "Done";
quit

