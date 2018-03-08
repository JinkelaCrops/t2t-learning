#!/usr/bin/env bash

TASK=med_test
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=google

# term process
python analyzerencode.py -f $TMP_DIR/$FILE_NAME --report 100000

# segment
python segment.py -f $TMP_DIR/$FILE_NAME.decode -l en

# src gen
python analyzerdecode.py -f $TMP_DIR/$FILE_NAME.decode -d $TMP_DIR/$FILE_NAME.dict -t $TMP_DIR/encode.$FILE_NAME.decode

