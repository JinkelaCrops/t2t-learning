#!/usr/bin/env bash

source activate py36

TASK=med_test
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=src.test.txt

## term pool
python analyzerencode.py -f $TMP_DIR/$FILE_NAME.en --report 100000
python analyzerencode.py -f $TMP_DIR/$FILE_NAME.zh --report 100000

# segment
python segment.py -f $TMP_DIR/$FILE_NAME.decode.en -l en
python segment.py -f $TMP_DIR/$FILE_NAME.decode.zh -l zh

# src gen
python analyzerdecode.py -f $TMP_DIR/$FILE_NAME.decode.en -d $TMP_DIR/$FILE_NAME.decode.en.dict -t $TMP_DIR/encode.$FILE_NAME.decode.en
python segment.py -f $TMP_DIR/encode.$FILE_NAME.decode.en -l en




