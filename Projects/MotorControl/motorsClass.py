#!/usr/bin/env python3

"""
  FILE:  motorsClass.py    MOTORS CLASS

  PURPOSE:  Motor commands with acceleration control

  METHODS:
    Motors(readingsPerSec=10)         # create single instance and single motor control thread
    set_ramp(dpsps=600)               # set ramp rate - default 600 DPS per Second takes 0.5 second for 0 to 300 DPS
    cancel()                          # stop motors gracefully, close motor control thread
    stop(blocking=False)              # come to graceful stop
    halt()                            # immediate stop uncontrolled
    forward(dps=egpg.speed)           # drive forward with given or default target speed and graceful start
    backward()                        # drive backward with given or default target speed and graceful start
    drive_cm(dist, blocking=True)     # drive distance centimeters with graceful start and stop
    drive_inches(dist, blocking=True) # drive distance inches with graceful start and stop
    right(dps=egpg.speed)             # turn right (Clockwise) with graceful start
    spin_right(dps=egpg.speed)        # spin right (Clockwise) with graceful start
    left(dps=egpg.speed)              # turn left (Counter-Clockwise) with graceful start
    spin_left(dps=egpg.speed)         # spin left (Counter-Clockwise) with graceful start

  CLASS VARS:
    ramp_rate default:600             # current ramp rate - default 600 DPS per second
    target_dps                        # current target speed
    last_ramp_dps                     # last commanded motor speed of ramp
    readingsPerSec default:10         # rate at which speed versus target is checked

  INTERNAL THREAD METHODS
    _pollMotors(readingsPerSec=10)     # motor control thread
    _rampTgtCurStep(target,current,rampStep)   # calculate next speed on ramp to target
    _setMotors(ldps,rdps)              # command motors to new speed
    _control()                         # dispatch to control method based on motorsMode
    _controlDrive()                    # monitor forward or backward mode
    _controlTravel()                   # monitor drive_cm and drive_inches mode
    _controlTurn()                     # monitor right and left mode
    _controlSpin()                     # monitor spin_right and spin_left
    _controlStop()                     # monitor ramping down to stopped
    _controlStopped()                  # called while motors are not running

  INTERNAL VARS
    _motorsMode
    _debugLevel   0=off 1=basic 99=all

"""

# ######## CLAMP #####
def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

# ####### SIGN #####
def sign(n):    # returns -1 if <0, 0 if 0, +1 if positive
    return cmp(n,0)


class Motors():

    # CLASS VARS (Avail to all instances)

