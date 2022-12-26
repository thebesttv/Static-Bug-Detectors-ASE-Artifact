#!/usr/bin/env bash

ROOT_DIR=/home/thebesttv/Static-Bug-Detectors-ASE-Artifact
BUG_FILE=$ROOT_DIR/data/found-bugs/nullaway.found
LOG_FILE=$ROOT_DIR/analyzers/results/nullaway-proj-reports/log

rm -f $LOG_FILE

cd $ROOT_DIR/analyzers/nullaway/bugswarm
python3 main.py $BUG_FILE bugswarm/images 1 |& tee $LOG_FILE
