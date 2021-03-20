#!/bin/bash

sudo cp /var/lib/rpimonitor/stat/*.rrd rpi_db_bkup
sudo chmod 666 rpi_db_bkup/*.rrd
echo "Done Copy of RPI-Monitor DBs to rpi_db_bkup"

