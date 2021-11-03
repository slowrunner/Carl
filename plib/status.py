#!/usr/bin/python3

# status.py    Basic Status (thread-safe)
#      import status provides printStatus(egpg,ds)
#      ./status.py    will print status once and exit
#
#      ./status.py -l (or -loop) will print status every 5 seconds
#      UNTIL voltage stays below LOW_BATTERY (8.1v) 4 times,
#      then will issue a shutdown
#
#      ./status.py -d will print status without distance sensor
#
#      ./status.py -h (or --help) will print usage
#
#      ./status.py -l -v N.N  will loop till N.N x4 times,
#                             then shutdown
#      ./status.py -l -n      will not shutdown, warn only
#
# After advice from some folks over at raspberrypi.org robotics forum,
# and thinking about the 168 NiMH cells in my 10 year old Prius,
# my target discharge depth is 15-20% remaining capacity.
# 2019-January: ran logBattV.py - 8hrs to yellow light,
#               a little more to "red and dead"
# The GoPiGo3 volt() function registered 8.1v at the 15-20% capacity point
# which would be 8.7v at the battery pack or 1.09v/cell.
# (GoPiGo3 reverse polarity protection diode drop of 0.6v)
# This will yield a little more than 6.5 hours of mindless contemplation
#     by my bot in its corner.  Sacrificing 45-90 minutes of immediate
#     gratification for longevity.
#
#
# July 2021: Removed IMU from Carl - commented out IMU init

# IMPORTS
import sys
sys.path
sys.path.append('/home/pi/Carl/plib')
import time
import signal
import os
import myPyLib
import speak
import myconfig
from datetime import datetime
import easygopigo3
import battery
import myDistSensor
import lifeLog
import runLog
import argparse
from my_safe_inertial_measurement_unit import SafeIMUSensor
import carlDataJson as carlData

# (8cells x 1.09) - 0.6 GoPiGo3 reverse protect diode
LOW_BATTERY_V = 8.1  
WARNING_DELTA_V = 0.1

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=", "").replace("\n", ""))


# Return Clock Freq as a character string
def getClockFreq():
    res = os.popen('vcgencmd measure_clock arm').readline()
    res = int(res.split("=")[1])
    if (res < 1000000000):
        res = str(res/1000000)+" MHz"
    else:
        res = '{:.2f}'.format(res/1000000000.0)+" GHz"
    return res


# Return throttled flags as a character string
#   0x10001  under-voltage 4.63v occurred / occurring
#   0x20002  freq-cap occurred / occurring
#   0x40004  Temp Throttled occurred / occurring
#   0x80008  SOFT_TEMPERATURE_LIMIT (default 60degC, boot/config.txt temp_soft_limit=70 to increase)

def getThrottled():
    res = os.popen('vcgencmd get_throttled').readline()
    return res.replace("\n", "")


def getUptime():
    res = os.popen('uptime').readline()
    return res.replace("\n", "")

def getRoomTemp(imu):
    roomTemp = (imu.safe_read_temperature() * 9.0/5.0 + 32.0) - 0.7
    return roomTemp

def getChargingState():
    printableCS = ["Unknown", "Not Charging", "Charging", "Trickle Charging"]
    return printableCS[carlData.getCarlData('chargingState')]

def getDockingState():
    printableDS = ["Unknown", "Not Docked", "Docked", "Manual Dock Requested", "Manual UnDock Requested", "Cabled"]
    return printableDS[carlData.getCarlData('dockingState')]

def printStatus(egpg, ds):
    print("\n********* CARL Basic STATUS *****")
    print("{} {}".format(datetime.now().date(), getUptime()))
    vBatt = egpg.volt()  # use thread-safe version not get_battery_voltage
    print("Battery Voltage: %0.2f" % vBatt)
    v5V = egpg.get_voltage_5v()
    # print("5v Supply: %0.2f" % v5V)
    print(battery.voltages_string(egpg))
    lifeRem = battery.hoursOfLifeRemaining(vBatt)
    lifeH = int(lifeRem)
    lifeM = (lifeRem-lifeH)*60
    print("Estimated Life Remaining: %d h %.0f m" % (lifeH, lifeM))
    print("Processor Temp: %s" % getCPUtemperature())
    try:
        print("Estimated Room Temp: %.1F" % getRoomTemp(egpg.imu))
    except Exception:  #no imu defined by user of printStatus
        pass
    print("Clock Frequency: %s" % getClockFreq())
    print("%s" % getThrottled())
    print("Docking State: {}".format(getDockingState()))
    print("Charging State: {}".format(getChargingState()))
    if ds is not None:
        dist = myDistSensor.adjustReadingInMMForError(ds.read_mm()) / 25.4
        if dist < 90:
            print("Distance Sensor: %0.1f inches" % dist)
        else:
            print("Distance Sensor: nothing within 90 inches")


# ##### MAIN ######


def handle_ctlc():
    print("status.py: handle_ctlc() executed")


def main():
    # #### SET CNTL-C HANDLER
    myPyLib.set_cntl_c_handler(handle_ctlc)

    # #### Create a mutex protected instance of EasyGoPiGo3 base class
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    myconfig.setParameters(egpg)
    # try:
    #     egpg.imu = SafeIMUSensor(port = "AD1", use_mutex = True, init = False)
    # except Exception: # no imu
    #     pass
    batteryLowCount = 0
    warningCount = 0

    # ARGUMENT PARSER
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--loop", default=False, action='store_true',
                    help="optional loop mode")
    ap.add_argument("-d", "--distance_sensor", default=True,
                    action='store_false', help="no distance sensor")
    ap.add_argument("-v", "--lowBattV", type=float, default=LOW_BATTERY_V,
                    help="Shutdown battery voltage limit")
    ap.add_argument("-n", "--noShutdown", default=False, action='store_true',
                    help="Will not shutdown, warning only")

    args = vars(ap.parse_args())
    loopFlag = args['loop']
    dsFlag = args['distance_sensor']
    lowBattV = args['lowBattV']
    noShutdown = args['noShutdown']

    # ### Create (protected) instance of EasyDistanceSensor
    if dsFlag:
        ds = myDistSensor.init(egpg)
    else:
        ds = None

    strStart = "Starting status.py at {0:0.2f}v".format(egpg.volt())
    print(strStart)
    if loopFlag:
        # runLog.logger.info(strStart)
        runLog.entry(strStart)

    # print ("Starting status loop at %.2f volts" % battery.volts())
    try:
        while True:
            time.sleep(5)
            printStatus(egpg, ds)
            vBatt = egpg.volt()
            if (lowBattV < vBatt < (lowBattV + WARNING_DELTA_V)):
                warningCount += 1
                if (warningCount % 12) == 1:
                    speak.say("Hello? My battery is getting a little low here.")
                    print("\nHello? My Battery is getting a little low here.")
            if (vBatt < lowBattV):
                if noShutdown is False:
                    batteryLowCount += 1
                speak.say("My battery is very low. Warning {}".format(batteryLowCount))
                print("\nMy Battery is very low. Warning {}".format(batteryLowCount))
            else:
                batteryLowCount = 0
            if (noShutdown is False) and (batteryLowCount > 3):
                speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
                lifeLog.logger.info(
                       "status.py safety shutdown at {0:0.2f}v".format(vBatt))
                print("BATTERY %.2f volts BATTERY LOW" % vBatt)
                print("BATTERY LOW - SHUTTING DOWN IN 1 MINUTE")
                time.sleep(1)
                os.system("sudo shutdown -h +1")
                sys.exit(0)
            if (loopFlag is False):
                break
        # end while
    except SystemExit:
        strToLog = "Exiting  status.py at {0:0.2f}v".format(egpg.volt())
        if loopFlag:
            # runLog.logger.info(strToLog)
            runLog.entry(strToLog)
        print(strToLog)
        time.sleep(1)


if __name__ == "__main__":
    main()
