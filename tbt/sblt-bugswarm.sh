ROOT_DIR=/home/thebesttv/Static-Bug-Detectors-ASE-Artifact
BUG_FILE=$ROOT_DIR/data/bugs/bugswarm.bugs
LOG_FILE=$ROOT_DIR/analyzers/results/sblt-proj-reports/log

rm -f $LOG_FILE

cd $ROOT_DIR/analyzers/spotbugs/bugswarm
python3 main.py $BUG_FILE bugswarm/images low 2 |& tee $LOG_FILE
