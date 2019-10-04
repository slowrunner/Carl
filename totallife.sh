#!/bin/bash
#
# totallife.sh    print total hours and sessions of life in life.log
#
# requires bc  (sudo apt-get install bc)
#

# awk -F':' '{sum+=$3}END{print "total life: " sum " hrs";}' life.log
totalLife=`(awk -F':' '{sum+=$3}END{print sum;}' life.log)`
echo "Total Life: " $totalLife "hrs"
lifeThisYear=`(awk -F':' 'FNR > 6 {sum+=$3}END{print sum;}' life.log)`
echo "Life this year: " $lifeThisYear
# echo "Sessions (boot) this year: " `(grep -c "\- boot \-" life.log)`
bootedThisYr=`(grep -c "\- boot \-" life.log)`
echo "Sessions (boot) this year: " $bootedThisYr
aveSession=`(echo "scale=0; $lifeThisYear / $bootedThisYr" | bc)`
echo "Average Time Between Reboot: " $aveSession
lastDockingStr=`(grep "h playtime" life.log | tail -1)`
totalDockings=`(awk -F"Docking " '{sub(/ .*/,"",$2);print $2}' <<< $lastDockingStr)`
echo "Total Dockings: " $totalDockings
dockingsThisYear=`(grep -c "h playtime" life.log)`
echo "Dockings this year: " $dockingsThisYear
# echo "Last Docking: " `(grep "h playtime" life.log | tail -1)`
aveCycleTimeTotal=`(echo "scale=1; $totalLife / $totalDockings" | bc)`
echo "Ave Cycle total life: " $aveCycleTimeTotal "hours"
aveCycleTime=`(echo "scale=1; $lifeThisYear / $dockingsThisYear" | bc)`
echo "Ave Cycle this year: " $aveCycleTime "hours"
echo "Last Docking: " $lastDockingStr
echo "Last Recharge: " `(grep Dismount life.log | tail -1)`
