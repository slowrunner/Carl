#!/bin/bash

fn="healthCheck.py"
echo "diff local "$fn" with plib version"
diff $fn ~/Carl/plib/$fn
fn="resetGoPiGo3.py"
echo "diff local "$fn" with plib version"
diff $fn ~/Carl/plib/$fn
echo "No Difference If Nothing Listed"
