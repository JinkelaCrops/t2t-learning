#!/usr/bin/env bash

source activate py36

TASK=tmxmall_med
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=Tmxmall医学语料_en-US_zh-CN_zh-CN_en-US.txt

# filter
python filter.py -f $TMP_DIR/$FILE_NAME

# unpack
python unpack.py -f $TMP_DIR/filter.$FILE_NAME

# segment
python segment.py -f $TMP_DIR/filter.$FILE_NAME.zh -l zh -p 10000
python segment.py -f $TMP_DIR/filter.$FILE_NAME.en -l en -p 10000
