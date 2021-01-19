#!/bin/bash

echo "Release to Carl/plib and model dir"

fn="hotword.py"
echo "Copying "$fn
cp $fn ~/Carl/plib

echo "Releasing model hey_carl_v1.2.3 to ~/Carl/nyuamay_engine_carl/models/Hotword"
cp nyumaya_models_carl/hey_carl_v1.2.3/* ~/Carl/nyumaya_engine_carl/models/Hotword/
echo "Done"
