#!/bin/bash

set -x

echo "Auto-observing and committing strava dump file at $(date)"

# Config
OBSERVER_DIR=/home/popcornisgood/TripDashObserver
TOKEN_FILE=token.json
CLIENT_CREDS_FILE=client_creds.json
BLOG_REPO_DIR=/home/popcornisgood/markbradley27.github.io
DUMP_FILE=debStravaDump.json

# Run observer
python $OBSERVER_DIR/observer.py --token_path $OBSERVER_DIR/$TOKEN_FILE --client_creds_path $OBSERVER_DIR/$CLIENT_CREDS_FILE

# Copy results to blog repo
cp $OBSERVER_DIR/$DUMP_FILE $BLOG_REPO_DIR/

# Blindly try to commit, if there aren't any updates, it won't work
git -C $BLOG_REPO_DIR reset \*
git -C $BLOG_REPO_DIR add $DUMP_FILE
git -C $BLOG_REPO_DIR commit -m "Auto-commit of debStravaDump at $(date)"
git -C $BLOG_REPO_DIR push origin master
