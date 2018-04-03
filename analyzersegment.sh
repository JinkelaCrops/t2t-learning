#!/usr/bin/env bash

TMP_DIR=$HOMEPATH/t2t_datagen/med_test/test
FILE_NAME=test.youdao

# term process
python analyzerencode.py -f $TMP_DIR/$FILE_NAME --report 100000

# segment
python segment.py -f $TMP_DIR/$FILE_NAME.decode -l en

# src gen
python analyzerdecode.py -f $TMP_DIR/seg.$FILE_NAME.decode \
                         -d $TMP_DIR/$FILE_NAME.decode.dict \
                         -t $TMP_DIR/encode.seg.$FILE_NAME.decode \
                         --dict_type json

cp $TMP_DIR/encode.seg.$FILE_NAME.decode $TMP_DIR/encode.$FILE_NAME

rm $TMP_DIR/*.decode
rm $TMP_DIR/*.dict

python mybleu.py -rf $TMP_DIR/encode.test -tf $TMP_DIR/encode.$FILE_NAME -l en --truncate 1000 --lower True
