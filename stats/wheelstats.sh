#!/bin/bash
#
# stats/wheelstats.sh    print total travel, rotation, travel time and segments of travel in wheel.log
#
# USAGE:
#  1) set year=
#  2) ./wheelstats.sh > wheelstats.year.x
#
# requires bc  (sudo apt-get install bc)
#              note bc scale only works for division
#
year=7
echo "WHEEL STATS for YEAR " $year
wfn="wheel.log.year.$year"
lfn="life.log.year.$year"
totalTravel=`(awk -F'travel:' '{sum+=sqrt($2^2)}END{printf "%.1f", sum/1000;}' $wfn)`
totalTravelFt=`(echo "scale=1; $totalTravel / 0.3048" | bc)`
echo "Total Travel: " $totalTravel "m" $totalTravelFt "ft"
totalRotate=`(awk -F'rotation:' '{sum+=sqrt($2^2)}END{printf "%.1f", sum;}' $wfn)`
totalRevs=`(echo "scale=1; $totalRotate / 360" | bc)`
echo "Total Rotate: " $totalRotate "deg" $totalRevs "revolutions"
totalMotion=`(awk -F'motion:' '{sum+=$2}END{printf "%.1f", sum;}' $wfn)`
totalMotionHrs=`(echo "scale=3; $totalMotion / 3600" | bc)`
echo "Total Motion: " $totalMotion "sec" $totalMotionHrs "hrs"
totalLife=`(awk -F':' '{sum+=$3}END{print sum;}' $lfn)`
percentInMotion=`(echo "scale=2; $totalMotionHrs * 100.0 / $totalLife" | bc)`
echo "Total Life: " $totalLife "hrs   percentInMotion:" $percentInMotion
lifeThisYear=`(awk -F':' 'FNR > 6 {sum+=$3}END{print sum;}' $lfn)`
# percentInMotion=`(echo "scale=2; $totalMotionHrs * 100.0 / $lifeThisYear" | bc)`
echo "Life this year: " $lifeThisYear "hrs (BOY Aug 22)"
