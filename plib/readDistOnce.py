#!/usr/bin/env python3

# FILE: readDistOnce.py

# PURPOSE:  Read Distance Sensor Once to check I2C bus operation

import sys
sys.path.insert(1,'/home/pi/Carl/plib')
import runLog
import easygopigo3
import myDistSensor

@runLog.logRun
def main():
	# Using plib version of easygopigo3 to get noinit feature
	egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)
	# egpg.tp = tiltpan.TiltPan(egpg)
	egpg.ds = egpg.init_distance_sensor("RPI_1")  # HW I2C
	# egpg.imu = SafeIMUSensor(port = "AD1", use_mutex = True)

	dist = egpg.ds.read_mm()
	adjDist = myDistSensor.adjustReadingInMMForError(dist)
	print(f"Distance Sensor Returned: {dist} mm")
	print("Corrected Distance: {:.0f} mm".format(adjDist))


if __name__ == '__main__': main()
