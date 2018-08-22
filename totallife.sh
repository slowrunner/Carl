#!/bin/bash
#
# totallife.sh    print total hours of life in life.log 
#

awk -F':' '{sum+=$3}END{print "total life: " sum "hrs";}' life.log

