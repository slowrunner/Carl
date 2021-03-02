#!/bin/bash

# Restore ChatScript to original git clone files
echo "Removing files from TMP/ USERS/ LOGS/ TOPIC/ to be per github"
rm TMP/*
rm USERS/*
rm LOGS/*
rm -rf TOPIC/*
echo "Restoring TOPIC/ per github"
cp -r TOPIC.bak/* TOPIC
echo "Done"
