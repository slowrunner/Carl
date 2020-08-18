#!/bin/bash

# Find latest dated files in given path
find $1 -type f -printf '%T@ %P\n' | sort -n | awk '{print $2}'
