#!/usr/bin/env bash

source activate py36

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

cd $TMP_DIR
cd ..
tar -cvf medicine/medicine.tar.gz medicine/train.en medicine/train.zh medicine/valid.en medicine/valid.zh



