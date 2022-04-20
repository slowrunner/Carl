# VIRTUAL BUMPERS FOR GoPiGo3 ROBOTS

The GoPiGo3 base robot does not include any bumper mechanism to detect collisions.

This Python module uses the GoPiGo3 intrinsic "Overloaded" sensing 
to create virtual front and rear bumpers.

# GET THE CODE:

wget https://raw.githubusercontent.com/slowrunner/Carl/master/Projects/virtualBumper/virtualbumper.py



# USAGE:

```
    from virtualbumper import VirtualBumper
    egpg = EasyGoPiGo3(use_mutex=True)
    egpg.bumper = VirtualBumper(egpg)
    BUMPER_CHECK_RATE = 20 # times per second (between 20 and 100 is good)
    SPEED = 3  # get_motor_status[3] is current wheel speed
for forward() or backward():
    drive_time = 2  # seconds
    egpg.forward()
    # Drive for drive_time,  unless bump into something
    for i in range(int(drive_time * BUMPER_CHECK_RATE)):
        if egpg.bumper.bumped() == True:
            egpg.stop()
            sleep(0.1)
            break
        sleep(1.0/BUMPER_CHECK_RATE)
or for drive_cm():
    drive_dist_cm = 25
    egpg.drive_cm(drive_dist_cm, blocking=False)
    # while wheels are turning, check if bumped into something
    while True:
        if egpg.bumper.bumped() == True:
            egpg.stop()
            break
        # check if reached target distance (both wheels stop)
        if (egpg.get_motor_status(egpg.MOTOR_LEFT)[SPEED] == 0) and (egpg.get_motor_status(egpg.MOTOR_RIGHT)[SPEED] == 0):
            break
        # sleep till time to check again
        sleep(1.0/BUMPER_CHECK_RATE)

```



