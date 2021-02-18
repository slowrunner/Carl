#!/bin/bash

echo "diff local with Carl/plib/ versions"
file="hotword.py"
echo "Comparing: "$file
diff $file ~/Carl/plib/$file
echo "No Differences If Nothing listed"

echo "Comparing local hey_carl model with ~/Carl/nyumaya_engine_carl/models/Hotword"
diff nyumaya_models_carl/hey_carl_v1.2.3/ ~/Carl/nyumaya_engine_carl/models/Hotword/
