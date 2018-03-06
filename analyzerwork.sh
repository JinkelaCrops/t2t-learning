#!/usr/bin/env bash

source activate py36

TASK=new_medicine
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=medicine.txt

# unpack
python unpack.py -f $TMP_DIR/$FILE_NAME -s " ||| "

# term pool
python analyzerpool.py -f $TMP_DIR/$FILE_NAME --report 100000

# analyzer datagen
python analyzerdatagen.py -f $TMP_DIR/$FILE_NAME --separator " ||| "

# traintestsplit
python analyzertrainvalidsplit.py -f $TMP_DIR/$FILE_NAME.term --valid_size 10000 --train_prefix $FILE_NAME.term.train --valid_prefix $FILE_NAME.term.test

## segment
python segment.py -f $TMP_DIR/$FILE_NAME.term.train.zh -l zh -p 10000 # --hanlp_path /home/tmxmall/hanlp
python segment.py -f $TMP_DIR/$FILE_NAME.term.train.en -l en -p 10000

#cp
cp $TMP_DIR/$FILE_NAME.term.train.dict $TMP_DIR/seg.$FILE_NAME.term.train.dict

# trainvalidsplit
python analyzertrainvalidsplit.py -f $TMP_DIR/seg.$FILE_NAME.term.train --valid_size 10000

# src test
python analyzerdecode.py -f $TMP_DIR/$FILE_NAME.term.test.zh -d $TMP_DIR/$FILE_NAME.term.test.dict -t $TMP_DIR/src.test.zh
python analyzerdecode.py -f $TMP_DIR/$FILE_NAME.term.test.en -d $TMP_DIR/$FILE_NAME.term.test.dict -t $TMP_DIR/src.test.en

cd $TMP_DIR
cd ..
tar -cvf $TASK/$TASK.tar.gz $TASK/train.en $TASK/train.zh $TASK/valid.en $TASK/valid.zh



