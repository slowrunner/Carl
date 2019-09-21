#!/bin/bash
#
# totallife.sh    print total hours and sessions of life in life.log
#

awk -F':' '{sum+=$3}END{print "total life: " sum " hrs";}' life.log
awk -F':' 'FNR > 6 {sum+=$3}END{print "life this year: " sum " hrs";}' life.log
echo "Sessions (boot) this year: " `(grep -c "\- boot \-" life.log)`
