# RPI-Monitor Databases

# Backing Up RPI-Monitor DBs ( to rpi_db_bkup/ )

./get_all_rpi_databases.sh

# Utility rrdtool

- To dump a dynamic value to xml

rrdtool dump carl_vbatt.rrd > carl_vbatt.xml

- To find a voltage entry

grep "v\>x" carl_vbatt.xml  (to find value X.)

or 

grep "e\-" carl_vbatt.xml  (to find value 0.X)
