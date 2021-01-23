#!/bin/bash

fn="voicecmdr.py"
echo "diff local "$fn" with plib version"
diff $fn ~/Carl/plib/$fn
fn="voiceLog.py"
echo "diff local "$fn" with plib version"
diff $fn ~/Carl/plib/$fn
echo "No Difference If Nothing Listed"
