\! echo "Executing list_users.sql";
use mysql;
\! echo "Existing Users"
SELECT User FROM mysql.user;
\! echo "";
\! echo "Done";
quit

