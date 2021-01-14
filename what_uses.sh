#!/bin/bash

# FILE:  what_uses.sh
# USAGE:  ./what_uses.sh "pattern"

if [ "$#" -ne 1 ] ;
	then echo "Usage:  ./what_uses.sh \"import xyz\" "
	exit
fi
echo "Searching to find what Python files use \"$1\" "
grep -r --include "*.py" "$1" .

