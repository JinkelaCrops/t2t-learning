#!/usr/bin/env bash

source activate py36

TASK=new_medicine
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=src.test

# term pool
python analyzerencode.py -f $TMP_DIR/$FILE_NAME --report 100000

# segment
python segment.py -f $TMP_DIR/$FILE_NAME.decode.en -l en
python segment.py -f $TMP_DIR/$FILE_NAME.decode.zh -l zh





