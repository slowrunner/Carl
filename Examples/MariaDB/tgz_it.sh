#!/bin/bash

mkdir MariaDBdemo
cp *.py MariaDBdemo
cp README.md MariaDBdemo
tar -zcvf MariaDBdemo.tgz MariaDBdemo
rm -r MariaDBdemo
echo "done"
