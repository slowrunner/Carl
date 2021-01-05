#!/bin/bash

# see https://github.com/alphacep/vosk-api
curl -L0 --output vosk-api/vosk-api.zip https://github.com/alphacep/vosk-api/archive/master.zip
cd vosk-api
unzip vosk-api.zip
cp vosk-api-master/python .
rm -rf vosk-api.zip vosk-api-master/

