#!/bin/bash

while true
do
    SUFFIX=$(date '+%Y-%m-%d-%H:%M:%S')
    cp data/teams.csv backup/teams-$SUFFIX.csv
    cp data/apl0.csv backup/apl0-$SUFFIX.csv
    sleep 60
done