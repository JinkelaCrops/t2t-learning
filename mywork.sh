#!/usr/bin/env bash

HOMEPATH=../t2t_med
TMP_DIR=$HOMEPATH/t2t_datagen/medicine

# filter
python filter.py -f $TMP_DIR/medicine.sample.txt -s " ||| "

# unpack
python unpack.py -f $TMP_DIR/filter.medicine.sample.txt -s " ||| "

# segment
python segment.py -f $TMP_DIR/filter.medicine.sample.txt.zh -l zh
python segment.py -f $TMP_DIR/filter.medicine.sample.txt.en -l en

# trainvalidsplit
python trainvalidsplit.py -f $TMP_DIR/seg.filter.medicine.sample.txt -z 1000

tar -cvPf $TMP_DIR/medicine.tar.gz $TMP_DIR/train.en $TMP_DIR/train.zh $TMP_DIR/valid.en $TMP_DIR/valid.zh



