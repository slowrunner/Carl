#!/bin/bash
#
# totallife.sh    print total hours and sessions of life in life.log
#
# requires bc  (sudo apt-get install bc)
#

awk -F':' '{sum+=$3}END{print "total life: " sum " hrs";}' life.log
lifeThisYear=`(awk -F':' 'FNR > 6 {sum+=$3}END{print sum;}' life.log)`
echo "Life this year: " $lifeThisYear
echo "Sessions (boot) this year: " `(grep -c "\- boot \-" life.log)`
dockingsThisYear=`(grep -c "h playtime" life.log)`
echo "Dockings this year: " $dockingsThisYear
echo "Last Docking: " `(grep "h playtime" life.log | tail -1)`
echo "Last Recharge: " `(grep Dismount life.log | tail -1)`
avePlaytime=`(echo "scale=1; $lifeThisYear / $dockingsThisYear" | bc)`
echo "Average playtime: " $avePlaytime "hours"
