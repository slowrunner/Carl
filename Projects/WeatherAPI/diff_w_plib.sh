#!/bin/bash

fn="weather.py"
echo "diff local "$fn" with plib version"
diff $fn ~/Carl/plib/$fn
echo "No Difference If Nothing Listed"
