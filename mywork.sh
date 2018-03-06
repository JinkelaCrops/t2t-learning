#!/usr/bin/env bash

source activate py36

HOMEPATH=/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449/t2t_med
TMP_DIR=$HOMEPATH/t2t_datagen/medicine
FILE_NAME=medicine.sample.big.txt

# filter
python filter.py -f $TMP_DIR/$FILE_NAME -s " ||| "

# unpack
python unpack.py -f $TMP_DIR/filter.$FILE_NAME -s " ||| "

# segment
python segment.py -f $TMP_DIR/filter.$FILE_NAME.zh -l zh -p 10000
python segment.py -f $TMP_DIR/filter.$FILE_NAME.en -l en -p 10000

# trainvalidsplit
python trainvalidsplit.py -f $TMP_DIR/seg.filter.$FILE_NAME -z 200

cd $TMP_DIR
cd ..
tar -cvf medicine/medicine.tar.gz medicine/train.en medicine/train.zh medicine/valid.en medicine/valid.zh



