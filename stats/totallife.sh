#!/bin/bash
#
# stats/totallife.sh    print total hours and sessions of life in life.log.year.x
#
# 1) set year=x
# 2) check newBattsAtCycle
# 3) ./totallife.sh > stats.year.x
#
# requires bc  (sudo apt-get install bc)
#
year=3
echo "TOTAL LIFE STATISTICS for YEAR " $year
fn="/home/pi/Carl/stats/life.log.year.$year"
# declare -i newBattsAtCycle=1453
declare -i newBattsAtCycle=2160
# awk -F':' '{sum+=$3}END{print "total life: " sum " hrs";}' $fn
totalLife=`(awk -F':' '{sum+=$3}END{print sum;}' $fn)`
echo "Total Life: " $totalLife "hrs since Aug 22,2018"
lifeThisYear=`(awk -F':' 'FNR > 6 {sum+=$3}END{print sum;}' $fn)`
echo "Life this year: " $lifeThisYear "hrs (BOY Aug 22)"
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
echo "New Batteries At Cycle:" $newBattsAtCycle
currentBattCycles=`(echo "scale=1; $totalDockings - $newBattsAtCycle" | bc)`
echo "Battery Set At Cycle: " $currentBattCycles
dockingFailures=`(grep -c "Docking Failure Possible" $fn)`
failurePercent=`(echo "scale=1; $dockingFailures * 100 / $dockingsThisYear" | bc)`
echo "Docking Failures this year: " $dockingFailures " or " $failurePercent "% of Dockings"
safetyShutdowns=`(grep -c "Safety Shutdown" $fn)`
safetyPercent=`(echo "scale=1; $safetyShutdowns * 100 / $dockingsThisYear" | bc)`
echo "Safety Shutdowns this year: " $safetyShutdowns " or " $safetyPercent "% of Dockings"
#aveCycleTimeTotal=`(echo "scale=1; $totalLife / $totalDockings" | bc)`
#echo "Ave Cycle total life: " $aveCycleTimeTotal "hours"
aveCycleTime=`(echo "scale=1; $lifeThisYear / ($dockingsThisYear - $dockingFailures)" | bc)`
echo "Ave Cycle this year (w/o failures): " $aveCycleTime "hours"

playtime=`(grep playtime $fn | awk -F"after" '{sum+=$2}END{print sum;}' )`
avePlaytime=`(echo "scale=1; $playtime / ($dockingsThisYear - $dockingFailures)" | bc)`
rechargeTime=`(grep recharge $fn | awk -F"after" '{sum+=$2}END{print sum;}' )`
aveRechargeTime=`(echo "scale=1; $rechargeTime / ($dockingsThisYear - $dockingFailures)" | bc)`
aveCycleTime=`(echo "scale=1; $avePlaytime + $aveRechargeTime" | bc)`
echo "Ave Cycle this year: " $aveCycleTime "hours"
echo "Ave Playtime this year: " $avePlaytime
last10recordNumber=`(echo "$dockingsThisYear - 10" | bc)`
# echo "last10recordNumber:" $last10recordNumber
last10playtimes=`(grep playtime $fn | tail -10 | awk -F"after"  '{sum+=$2}END{print sum;}' )`
# echo "last10playtimes" $last10playtimes
last10avePlaytime=`(echo "scale=1; $last10playtimes / 10" | bc)`
echo "Ave of Last 10 Playtimes" $last10avePlaytime
echo "Last Docking: " $lastDockingStr
echo "Last Recharge: " `(grep Dismount $fn | tail -1)`