\! echo "Executing drop_user.sql";
use mysql;
\! echo "Existing Users"
SELECT User FROM mysql.user;
\! echo " ";
\! echo "Droping User If Exists";
DROP USER IF EXISTS 'user2drop'@localhost;
FLUSH PRIVILEGES;
\! echo " ";
\! echo "User List Now"
SELECT User FROM mysql.user;
\! echo " ";
\! echo "Done";
quit

