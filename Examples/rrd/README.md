# RPI-Monitor Utility rrdtool

- To dump a dynamic value to xml

rrdtool dump carl_vbatt.rrd > carl_vbatt.xml

- To find a voltage entry

grep "v\>x" carl_vbatt.xml  (to find value X.)

or 

grep "e\-" carl_vbatt.xml  (to find value 0.X)
