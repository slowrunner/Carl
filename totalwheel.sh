#!/bin/bash
#
# totalwheel.sh    print total travel, rotation, travel time and segments of travel in wheel.log
#
# requires bc  (sudo apt-get install bc)
#
declare -i catchupSegmentss=1500
totalTravel=`(awk -F'travel:' '{sum+=sqrt($2^2)}END{print sum;}' wheel.log)`
totalTravelFt=`(echo "scale=1; $totalTravel / 304.8" | bc)`
echo "Total Travel: " $totalTravel "mm" $totalTravelFt "ft"
totalRotate=`(awk -F'rotation:' '{sum+=$2}END{print sum;}' wheel.log)`
totalRevs=`(echo "scale=1; $totalRotate / 360" | bc)`
echo "Total Rotate: " $totalRotate "deg" $totalRevs "revolutions"
totalMotion=`(awk -F'motion:' '{sum+=$2}END{print sum;}' wheel.log)`
totalMotionHrs=`(echo "scale=3; $totalMotion / 3600" | bc)`
echo "Total Motion: " $totalMotion "sec" $totalMotionHrs "hrs"
totalLife=`(awk -F':' '{sum+=$3}END{print sum;}' life.log)`
percentInMotion=`(echo "scale=2; $totalMotionHrs * 100.0 / $totalLife" | bc)`
echo "Total Life: " $totalLife "hrs   percentInMotion:" $percentInMotion
# lifeThisYear=`(awk -F':' 'FNR > 6 {sum+=$3}END{print sum;}' life.log)`
# echo "Life this year: " $lifeThisYear "hrs (BOY Aug 22)"
# echo "Sessions (boot) this year: " `(grep -c "\- boot \-" life.log)`
# bootedThisYr=`(grep "\- boot \-" life.log | sort -u -k1,1 | wc -l)`
# echo "Days Booted This Year: " $bootedThisYr
# aveSession=`(echo "scale=0; $lifeThisYear / $bootedThisYr" | bc)`
# echo "Average Time Between Reboot: " $aveSession "hrs"
# lastDockingStr=`(grep "h playtime" life.log | tail -1)`
# totalDockings=`(awk -F"Docking " '{sub(/ .*/,"",$2);print $2}' <<< $lastDockingStr)`
# echo "Total Dockings: " $totalDockings
# dockingsThisYear=`(grep -c "h playtime" life.log)`
# echo "Dockings this year: " $dockingsThisYear
# echo "New Batteries At Cycle:" $newBattsAtCycle
# currentBattCycles=`(echo "scale=1; $totalDockings - $newBattsAtCycle" | bc)`
# echo "Battery Set At Cycle: " $currentBattCycles
# dockingFailures=`(grep -c "Docking Failure Possible" life.log)`
# failurePercent=`(echo "scale=1; $dockingFailures * 100 / $dockingsThisYear" | bc)`
# echo "Docking Failures this year: " $dockingFailures " or " $failurePercent "% of Dockings"
# aveCycleTimeTotal=`(echo "scale=1; $totalLife / $totalDockings" | bc)`
# echo "Ave Cycle total life: " $aveCycleTimeTotal "hours"
# aveCycleTime=`(echo "scale=1; $lifeThisYear / ($dockingsThisYear - $dockingFailures)" | bc)`
# echo "Ave Cycle this year (w/o failures): " $aveCycleTime "hours"

# playtime=`(grep playtime life.log | awk -F"after" '{sum+=$2}END{print sum;}' )`
# avePlaytime=`(echo "scale=1; $playtime / ($dockingsThisYear - $dockingFailures)" | bc)`
# rechargeTime=`(grep recharge life.log | awk -F"after" '{sum+=$2}END{print sum;}' )`
# aveRechargeTime=`(echo "scale=1; $rechargeTime / ($dockingsThisYear - $dockingFailures)" | bc)`
# aveCycleTime=`(echo "scale=1; $avePlaytime + $aveRechargeTime" | bc)`
# echo "Ave Cycle this year: " $aveCycleTime "hours"
# echo "Ave Playtime this year: " $avePlaytime
# echo "Last Docking: " $lastDockingStr
# echo "Last Recharge: " `(grep Dismount life.log | tail -1)`
