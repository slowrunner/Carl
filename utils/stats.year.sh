#!/bin/bash
#
# stats.year.sh    print total hours and sessions of life in life.log.year.2
#
# requires bc  (sudo apt-get install bc)
#
# fn: life.log file to use for statistics
fn='life.log.year.2'
# declare -i newBattsAtCycle=233
#
# awk -F':' '{sum+=$3}END{print "total life: " sum " hrs";}' life.log
totalLife=`(awk -F':' '{sum+=$3}END{print sum;}' $fn)`
echo "Total Life: " $totalLife "hrs"
lifeThisYear=`(awk -F':' 'FNR > 6 {sum+=$3}END{print sum;}' $fn)`
pctOfYear=`(echo "scale=1; $lifeThisYear * 100 / 8760 " | bc)`
echo "Life this year: " $lifeThisYear "hrs (BOY Aug 22)"
echo "Operational: " $pctOfYear"% of year"
# echo "Sessions (boot) this year: " `(grep -c "\- boot \-" $fn)`
bootedThisYr=`(grep "\- boot \-" $fn | sort -u -k1,1 | wc -l)`
echo "Days Booted This Year: " $bootedThisYr
aveSession=`(echo "scale=0; $lifeThisYear / $bootedThisYr" | bc)`
echo "Average Time Between Reboot: " $aveSession "hrs"
lastDockingStr=`(grep "h playtime" $fn | tail -1)`
totalDockings=`(awk -F"Docking " '{sub(/ .*/,"",$2);print $2}' <<< $lastDockingStr)`
echo "Total Dockings: " $totalDockings
dockingsThisYear=`(grep -c "h playtime" $fn)`
echo "Dockings this year: " $dockingsThisYear
# echo "New Batteries At Cycle:" $newBattsAtCycle
# currentBattCycles=`(echo "scale=1; $totalDockings - $newBattsAtCycle" | bc)`
# echo "Battery Set At Cycle: " $currentBattCycles
dockingFailures=`(grep -c "Docking Failure Possible" $fn)`
failurePercent=`(echo "scale=1; $dockingFailures * 100 / $dockingsThisYear" | bc)`
echo "Docking Failures this year: " $dockingFailures " or " $failurePercent "% of Dockings"
# aveCycleTimeTotal=`(echo "scale=1; $totalLife / $totalDockings" | bc)`
# echo "Ave Cycle total life: " $aveCycleTimeTotal "hours"
aveCycleTime=`(echo "scale=1; $lifeThisYear / ($dockingsThisYear - $dockingFailures)" | bc)`
echo "Ave Cycle this year (w/o failures): " $aveCycleTime "hours"
#
playtime=`(grep playtime $fn | awk -F"after" '{sum+=$2}END{print sum;}' )`
avePlaytime=`(echo "scale=1; $playtime / ($dockingsThisYear - $dockingFailures)" | bc)`
rechargeTime=`(grep recharge $fn | awk -F"after" '{sum+=$2}END{print sum;}' )`
aveRechargeTime=`(echo "scale=1; $rechargeTime / ($dockingsThisYear - $dockingFailures)" | bc)`
aveCycleTime=`(echo "scale=1; $avePlaytime + $aveRechargeTime" | bc)`
echo "Ave Cycle this year: " $aveCycleTime "hours"
echo "Ave Playtime this year: " $avePlaytime
echo "Last Docking: " $lastDockingStr
echo "Last Recharge: " `(grep Dismount $fn | tail -1)`
