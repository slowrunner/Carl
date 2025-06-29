#!/usr/bin/python3

# import gopigo3
# import easygopigo3
import sys
sys.path.append('/home/pi/Carl/plib')
from noinit_easygopigo3 import EasyGoPiGo3

import time
import math

DEBUG = True
rad_to_deg = 180.0/math.pi

def get_raw_LR_encoders(gpg):

    """
    Read left and right raw encoder values (in ticks)
    For 16-tick GoPiGo3: 1920 ticks per 360 degree wheel revolution
    (For 6-tick GoPiGo3:  720 ticks per 360 degree wheel rev)
    """

    l = gpg.spi_read_32(gpg.SPI_MESSAGE_TYPE.GET_MOTOR_ENCODER_LEFT)
    if DEBUG:
        print("left value read: {}".format(l))
    if l & 0x80000000:
        l = int(l - 0x100000000)

    r = gpg.spi_read_32(gpg.SPI_MESSAGE_TYPE.GET_MOTOR_ENCODER_RIGHT)
    if DEBUG:
        print("right value read: {}".format(r))

    if r & 0x80000000:
        r = int(r - 0x100000000)

    return l,r

def get_LR_encoders_in_degrees(gpg):
    """
    Read left and right gopigo3 API encoder values (in degrees)
    """
    l = gpg.get_motor_encoder(gpg.MOTOR_LEFT)
    r = gpg.get_motor_encoder(gpg.MOTOR_RIGHT)
    return l,r

def dHeading_API_in_degrees(end_l, end_r, start_l, start_r, gpg):

    dl = (end_l - start_l) / 360 * gpg.WHEEL_CIRCUMFERENCE
    dr = (end_r - start_r) / 360 * gpg.WHEEL_CIRCUMFERENCE
    dHeading_rad = (dr-dl) / gpg.WHEEL_BASE_WIDTH
    dHeading_deg = dHeading_rad * 180.0 / math.pi 
    return dHeading_deg

def dHeading_raw_in_radians(end_l, end_r, start_l, start_r, gpg):

    dl = (end_l - start_l) / 1920 * gpg.WHEEL_CIRCUMFERENCE
    dr = (end_r - start_r) / 1920 * gpg.WHEEL_CIRCUMFERENCE
    dHeading_rad = (dr-dl) / gpg.WHEEL_BASE_WIDTH
    return dHeading_rad

def  main():
    egpg = EasyGoPiGo3(use_mutex=True, noinit=True)
    egpg.set_speed(150)

    test_distance_cm = 100  # 1m
    test_turn_deg = 180

    print("Reset Encoders")
    egpg.reset_encoders()
    raw_heading = 0
    api_heading = 0

    start_raw_lenc, start_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(start_raw_lenc, start_raw_renc))
    start_deg_lenc, start_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(start_deg_lenc, start_deg_renc))
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))


    print("\nDrive {}cm".format(test_distance_cm))
    egpg.drive_cm(test_distance_cm)

    end_raw_lenc, end_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(end_raw_lenc, end_raw_renc))
    end_deg_lenc, end_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(end_deg_lenc, end_deg_renc))
    raw_heading = dHeading_raw_in_radians(end_raw_lenc, end_raw_renc, start_raw_lenc, start_raw_renc, egpg)
    api_heading = dHeading_API_in_degrees(end_deg_lenc, end_deg_renc, start_deg_lenc, start_deg_renc, egpg)
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))

    print("\nSleeping 60s ...")
    time.sleep(60)


    print("\nReset Encoders")
    egpg.reset_encoders()
    raw_heading = 0
    api_heading = 0

    start_raw_lenc, start_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(start_raw_lenc, start_raw_renc))
    start_deg_lenc, start_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(start_deg_lenc, start_deg_renc))
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))


    print("\nTurn {} deg".format(test_turn_deg))
    egpg.turn_degrees(test_turn_deg)

    end_raw_lenc, end_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(end_raw_lenc, end_raw_renc))
    end_deg_lenc, end_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(end_deg_lenc, end_deg_renc))
    raw_heading = dHeading_raw_in_radians(end_raw_lenc, end_raw_renc, start_raw_lenc, start_raw_renc, egpg)
    api_heading = dHeading_API_in_degrees(end_deg_lenc, end_deg_renc, start_deg_lenc, start_deg_renc, egpg)
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))


    print("\nSleeping 60s ...")
    time.sleep(60)


    print("\nReset Encoders")
    egpg.reset_encoders()
    raw_heading = 0
    api_heading = 0

    start_raw_lenc, start_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(start_raw_lenc, start_raw_renc))
    start_deg_lenc, start_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(start_deg_lenc, start_deg_renc))
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))


    print("\nTurn back {} deg".format(-test_turn_deg))
    egpg.turn_degrees(-test_turn_deg)

    end_raw_lenc, end_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(end_raw_lenc, end_raw_renc))
    end_deg_lenc, end_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(end_deg_lenc, end_deg_renc))
    raw_heading = dHeading_raw_in_radians(end_raw_lenc, end_raw_renc, start_raw_lenc, start_raw_renc, egpg)
    api_heading = dHeading_API_in_degrees(end_deg_lenc, end_deg_renc, start_deg_lenc, start_deg_renc, egpg)
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))


    print("\nSleeping 60s ...")
    time.sleep(60)


    print("\nReset Encoders")
    egpg.reset_encoders()
    raw_heading = 0
    api_heading = 0

    start_raw_lenc, start_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(start_raw_lenc, start_raw_renc))
    start_deg_lenc, start_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(start_deg_lenc, start_deg_renc))
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))


    print("\nDrive backward {}cm".format(-test_distance_cm))
    egpg.drive_cm(-test_distance_cm)

    end_raw_lenc, end_raw_renc = get_raw_LR_encoders(egpg)
    print("Raw Encoders (l,r) ({},{})".format(end_raw_lenc, end_raw_renc))
    end_deg_lenc, end_deg_renc = get_LR_encoders_in_degrees(egpg)
    print("API Encoders (l,r) ({},{} degrees)".format(end_deg_lenc, end_deg_renc))
    raw_heading = dHeading_raw_in_radians(end_raw_lenc, end_raw_renc, start_raw_lenc, start_raw_renc, egpg)
    api_heading = dHeading_API_in_degrees(end_deg_lenc, end_deg_renc, start_deg_lenc, start_deg_renc, egpg)
    print("raw_heading {:.2f} rad {:.1f} deg  api_heading {:.1f} deg".format(raw_heading, raw_heading*rad_to_deg, api_heading))




if __name__ =='__main__':
    main()

