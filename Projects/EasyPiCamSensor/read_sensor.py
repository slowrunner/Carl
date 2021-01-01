#!/usr/bin/env python3

# File: read_sensor.py

# Usage: ./read_sensor.py

# Reads all sensor readings 10 times per second for printing

# Uses Pi Camera via the EasyPiCamSensor class get_all_data() method
#     which returns a dictionary of all per frame updated data

import traceback

try:
    import easypicamsensor
except:
    print("Could not locate easypicamsensor.py")
    traceback.print_exc()
    exit(1)

import time


def print_w_date_time(alert):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    print("{} read_sensor: {}".format(time_now, alert))

def print_all_data(readings):
    alert = str(readings)
    print_w_data_time(alert)

def main():

    print_w_date_time("Starting")
    print_w_date_time("Warming Up The Camera")
    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
    print_w_date_time("Starting Loop")
    linecount = 0
    while True:
        try:
            linecount += 1
            if ((linecount % 15)==1):
                print("xmove ymov     latch_move_time     l_x   l_y       frame_time         rgb  (   values  )  dist    hsv  (       values       )   dist  left   whole  right (maxAng   val )")
            rd = epcs.get_all_data()   # get all updated-by-frame data in a dictionary
            readings_line = "{:>5s} {:>4s} {:>22s} {:>5s} {:>4s} {:>22s} {:>6s} ({:>3d},{:>3d},{:3d}) {:>6.2f} {:>6s} ({:>6.2f},{:>6.2f},{:>6.2f}) {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f} ({:>6.2f},{:>6.2f})".format(
                           rd["x_move"],
                                  rd["y_move"],
                                         str(rd["latch_move_time"])[:-4],
                                                 rd["latch_x_move"],
                                                        rd["latch_y_move"],
                                                               str(rd["dt_frame"])[:-4],
                                                                             rd["color_rgb"],
                                                                                   rd["color_ave_rgb"][0], rd["color_ave_rgb"][1], rd["color_ave_rgb"][2],
                                                                                       rd["color_dist_rgb"],
                                                                                             rd["color_hsv"],
                                                                                                   rd["color_ave_hsv"][0], rd["color_ave_hsv"][1], rd["color_ave_hsv"][2],
                                                                                                        rd["color_dist_hsv"],
                                                                                                                 rd["light_left_ave_intensity"],
                                                                                                                        rd["light_ave_intensity"],
                                                                                                                             rd["light_right_ave_intensity"],
                                                                                                                                      rd["light_max_deg_val"][0],
                                                                                                                                            rd["light_max_deg_val"][1] )
            print(readings_line)
            time.sleep(0.1)    # wait between checks
        except KeyboardInterrupt:
            break

    alert = "Sure.  Exiting stage right."
    print("\n")  # move to new line after ^C
    print_w_date_time(alert)


if __name__ == '__main__': main()
