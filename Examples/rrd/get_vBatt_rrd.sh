#!/bin/bash

sudo cp /var/lib/rpimonitor/stat/carl_vbatt.rrd .
sudo chmod 777 *.rrd
rrdtool dump carl_vbatt.rrd  > carl_vbatt.xml
