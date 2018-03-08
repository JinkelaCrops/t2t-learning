#!/usr/bin/env bash

TMP_DIR=$HOMEPATH/t2t_datagen/med_test/valid1
FILE_NAME=valid1.t2t_lstm_attention_bpe

# term process
python analyzerencode.py -f $TMP_DIR/$FILE_NAME --report 100000

# segment
python segment.py -f $TMP_DIR/$FILE_NAME.decode -l en

# src gen
python analyzerdecode.py -f $TMP_DIR/seg.$FILE_NAME.decode -d $TMP_DIR/$FILE_NAME.decode.dict -t $TMP_DIR/encode.seg.$FILE_NAME.decode

cp $TMP_DIR/encode.seg.$FILE_NAME.decode $TMP_DIR/encode.$FILE_NAME

rm $TMP_DIR/*.decode
rm $TMP_DIR/*.dict

# python mybleu.py -rf $HOMEPATH/t2t_datagen/med_test/valid1/encode.valid1 -tf $HOMEPATH/t2t_datagen/med_test/valid1/encode.valid1.google --truncate 1000 --lower True
