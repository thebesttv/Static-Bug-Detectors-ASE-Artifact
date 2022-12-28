#!/usr/bin/env bash

ROOT_DIR=/home/thebesttv/Static-Bug-Detectors-ASE-Artifact
BUG_FILE=$ROOT_DIR/tbt/bugs/eradicate-bugswarm.found
LOG_FILE=$ROOT_DIR/analyzers/results/eradicate-proj-reports/.log

rm -f $LOG_FILE

cd $ROOT_DIR/analyzers/eradicate/bugswarm
python3 main.py $BUG_FILE failed bugswarm/images |& tee -a $LOG_FILE
python3 main.py $BUG_FILE passed bugswarm/images |& tee -a $LOG_FILE
