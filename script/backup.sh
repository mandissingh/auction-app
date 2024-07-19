#!/bin/bash

SUFFIX=$(date '+%Y-%m-%d-%H:%M:%S')

mkdir backup
cp data/teams.csv backup/teams-$SUFFIX.csv
cp data/alpine0.csv backup/alpine0-$SUFFIX.csv