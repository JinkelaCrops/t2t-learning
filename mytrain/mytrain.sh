#!/usr/bin/env bash

export PYTHONPATH="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2:$PYTHONPATH"

$TMP_DIR="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2/test/medicine.sample"

# merge data if need
python mytrain/my_merge.py -i $TMP_DIR
# split test
python mytrain/my_split.py -f $TMP_DIR.data/data --train_name data --valid_name test --valid_size 100

## Step 1
## data filter
#python filter.py -f $TMP_DIR/data -s " ||| "
## train valid split
#python easysplit.py -f $TMP_DIR/data.filter --train step1.train --valid step1.valid --valid_size 10000 --shuffle True
## unpack data filter train, valid
#python unpack.py -f $TMP_DIR/step1.train -s " ||| "
#python unpack.py -f $TMP_DIR/step1.valid -s " ||| "
## segment
#python segment.py -f $TMP_DIR/step1.train.zh -l zh -p 10000 --to_file_name train.zh
#python segment.py -f $TMP_DIR/step1.train.en -l en -p 10000 --to_file_name train.en
#python segment.py -f $TMP_DIR/step1.valid.zh -l zh -p 10000 --to_file_name valid.zh
#python segment.py -f $TMP_DIR/step1.valid.en -l en -p 10000 --to_file_name valid.en
## keep valid src
#cp $TMP_DIR/step1.valid.en $TMP_DIR/valid.src.en.step1
#cp $TMP_DIR/step1.valid.zh $TMP_DIR/valid.src.zh.step1
## move to medicine
#mkdir $TMP_DIR/medicine -p
#mv $TMP_DIR/train.* --target-directory=$TMP_DIR/medicine
#mv $TMP_DIR/valid.* --target-directory=$TMP_DIR/medicine
## clean
#rm $TMP_DIR/step1.*

# Step 2
# data encode, use processpool, change data to data.origin
python analyzerpoolexecute.py -f $TMP_DIR/data -s " ||| " --file_process_size 5000 --workers 10
# term filter
python analyzerfilter.py -f $TMP_DIR/data.origin -zhf $TMP_DIR/data.zh.encode -enf $TMP_DIR/data.en.encode -zhd $TMP_DIR/data.zh.encode.dict -end $TMP_DIR/data.en.encode.dict
# train valid split
python easysplit.py -f $TMP_DIR/data.origin.term_filter --train step2.train.src --valid step2.valid.src --valid_size 10000 --shuffle True
python easysplit.py -f $TMP_DIR/data.zh.encode.term_filter --train step2.train.zh --valid step2.valid.zh --valid_size 10000 --shuffle True
python easysplit.py -f $TMP_DIR/data.en.encode.term_filter --train step2.train.en --valid step2.valid.en --valid_size 10000 --shuffle True
# unpack valid
python unpack.py -f $TMP_DIR/step2.valid.src -s " ||| "
# segment
python segment.py -f $TMP_DIR/step2.train.zh -l zh -p 10000 --to_file_name train.zh
python segment.py -f $TMP_DIR/step2.train.en -l en -p 10000 --to_file_name train.en
python segment.py -f $TMP_DIR/step2.valid.zh -l zh -p 10000 --to_file_name valid.zh
python segment.py -f $TMP_DIR/step2.valid.en -l en -p 10000 --to_file_name valid.en
# keep valid src
cp $TMP_DIR/step2.valid.src.en $TMP_DIR/valid.src.en.step2
cp $TMP_DIR/step2.valid.src.zh $TMP_DIR/valid.src.zh.step2
# move to medicine
mkdir $TMP_DIR/new_medicine -p
mv $TMP_DIR/train.* --target-directory=$TMP_DIR/new_medicine
mv $TMP_DIR/valid.* --target-directory=$TMP_DIR/new_medicine
## clean
rm $TMP_DIR/step2.*
rm $TMP_DIR/data.en.*
rm $TMP_DIR/data.zh.*

# Step 3
# data encode, use processpool, change data to data.origin
python analyzerpoolexecute.py -f $TMP_DIR/data -s " ||| " --file_process_size 5000 --workers 10
# train valid split
python easysplit.py -f $TMP_DIR/data.origin --train step3.train.src --valid step3.valid.src --valid_size 10000 --shuffle True
python easysplit.py -f $TMP_DIR/data.zh.encode --train step3.train.zh --valid step3.valid.zh --valid_size 10000 --shuffle True
python easysplit.py -f $TMP_DIR/data.en.encode --train step3.train.en --valid step3.valid.en --valid_size 10000 --shuffle True
# unpack valid
python unpack.py -f $TMP_DIR/step3.valid.src -s " ||| "
# segment
python segment.py -f $TMP_DIR/step3.train.zh -l zh -p 10000 --to_file_name train.zh
python segment.py -f $TMP_DIR/step3.train.en -l en -p 10000 --to_file_name train.en
python segment.py -f $TMP_DIR/step3.valid.zh -l zh -p 10000 --to_file_name valid.zh
python segment.py -f $TMP_DIR/step3.valid.en -l en -p 10000 --to_file_name valid.en
# keep valid src
cp $TMP_DIR/step3.valid.src.en $TMP_DIR/valid.src.en.step3
cp $TMP_DIR/step3.valid.src.zh $TMP_DIR/valid.src.zh.step3
# move to medicine
mkdir $TMP_DIR/new_medicine -p
mv $TMP_DIR/train.* --target-directory=$TMP_DIR/new_medicine
mv $TMP_DIR/valid.* --target-directory=$TMP_DIR/new_medicine
## clean
rm $TMP_DIR/step3.*
rm $TMP_DIR/data.en.*
rm $TMP_DIR/data.zh.*