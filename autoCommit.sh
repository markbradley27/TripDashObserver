#!/bin/bash

echo "Auto-observing and committing strava dump file at $(date)"

# Config
OBSERVERDIR=/home/ubuntu/GitRepos/TripDashObserver
BLOGREPODIR=/home/ubuntu/GitRepos/markbradley27.github.io
DUMPFILE=stravaDump.json

# Run observer
python $OBSERVERDIR/observer.py

# Copy results to blog repo
cp $OBSERVERDIR/$DUMPFILE $BLOGREPODIR/

# Blindly try to commit, if there aren't any updates, it won't work
git -C $BLOGREPODIR reset *
git -C $BLOGREPODIR add $DUMPFILE
git -C $BLOGREPODIR commit -m "Auto-commit of stravaDump at $(date)"
git -C $BLOGREPODIR push origin master
