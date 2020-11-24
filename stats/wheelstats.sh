#!/bin/bash
#
# wheelstats.sh    print total travel, rotation, travel time and segments of travel in wheel.log
#
# requires bc  (sudo apt-get install bc)
#
echo "WHEEL STATS"
# declare -i catchupSegmentss=1500
wfn="wheel.log.year.2"
lfn="life.log.year.2"
declare -i priorTravel=
declare -i priorRotation=
declare -i priorMotionsec=
#
# YEAR 1
# WHEEL STATS
# Total Travel:  461262 mm 1513.3 ft
# Total Rotate:  459360 deg 1276.0 revolutions
# Total Motion:  11233 sec 3.120 hrs
# Total Life:  3389.37 hrs   percentInMotion: .09
# totalTravel=`(awk -F'travel:' '{sum+=sqrt($2^2)}END{print sum;}' $wfn)`

totalTravelFt=`(echo "scale=1; $totalTravel / 304.8" | bc)`
echo "Total Travel: " $totalTravel "mm" $totalTravelFt "ft"
totalRotate=`(awk -F'rotation:' '{sum+=$2}END{print sum;}' $wfn)`
totalRevs=`(echo "scale=1; $totalRotate / 360" | bc)`
echo "Total Rotate: " $totalRotate "deg" $totalRevs "revolutions"
totalMotion=`(awk -F'motion:' '{sum+=$2}END{print sum;}' $wfn)`
totalMotionHrs=`(echo "scale=3; $totalMotion / 3600" | bc)`
echo "Total Motion: " $totalMotion "sec" $totalMotionHrs "hrs"
# totalLife=`(awk -F':' '{sum+=$3}END{print sum;}' $lfn)`
# percentInMotion=`(echo "scale=2; $totalMotionHrs * 100.0 / $totalLife" | bc)`
# echo "Total Life: " $totalLife "hrs   percentInMotion:" $percentInMotion
lifeThisYear=`(awk -F':' 'FNR > 6 {sum+=$3}END{print sum;}' $lfn)`
"Life this year: " $lifeThisYear "hrs (BOY Aug 22)"
percentInMotion=`(echo "scale=2; $totalMotionHrs * 100.0 / $ifeThisYear" | bc)`
