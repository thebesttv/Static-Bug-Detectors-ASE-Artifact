#!/usr/bin/env bash

ROOT_DIR=/home/thebesttv/Static-Bug-Detectors-ASE-Artifact
BUG_FILE=$ROOT_DIR/tbt/bugs/cfnullness-bugswarm.found
LOG_FILE=$ROOT_DIR/analyzers/results/checkerframework-proj-reports/log

rm -f $LOG_FILE

cd $ROOT_DIR/analyzers/checker-framework/bugswarm
python3 main.py $BUG_FILE bugswarm/images 1 |& tee $LOG_FILE
