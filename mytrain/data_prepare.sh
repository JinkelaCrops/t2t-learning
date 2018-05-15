#!/usr/bin/env bash

#export PYTHONPATH="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2:$PYTHONPATH"
#CODE_DIR="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2"
#TMP_DIR="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2/test/medicine.sample"
export PYTHONPATH="/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2:$PYTHONPATH"
CODE_DIR="/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2"
TMP_DIR="/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2/test/medicine.sample"

cd $CODE_DIR

# merge data if need
python mytrain/my_merge.py -i $TMP_DIR
# split test
python mytrain/my_split.py -f $TMP_DIR.data/data --train_name data --valid_name test --valid_size 100
# term filter
python mytrain/my_filter.py -f $TMP_DIR.data/data.data -sep " ||| "
# train valid split
python mytrain/my_split.py -f $TMP_DIR.data.filter/data.data.origin          --train_name train --valid_name valid --valid_size 100
python mytrain/my_split.py -f $TMP_DIR.data.filter/data.data.src.encode      --train_name train --valid_name valid --valid_size 100
python mytrain/my_split.py -f $TMP_DIR.data.filter/data.data.src.encode.dict --train_name train --valid_name valid --valid_size 100
python mytrain/my_split.py -f $TMP_DIR.data.filter/data.data.tgt.encode      --train_name train --valid_name valid --valid_size 100
python mytrain/my_split.py -f $TMP_DIR.data.filter/data.data.tgt.encode.dict --train_name train --valid_name valid --valid_size 100
# segment
python mytrain/my_segment.py -f $TMP_DIR.data.filter/data.data.src.encode.train -lan zh
python mytrain/my_segment.py -f $TMP_DIR.data.filter/data.data.src.encode.valid -lan zh
python mytrain/my_segment.py -f $TMP_DIR.data.filter/data.data.tgt.encode.train -lan en
python mytrain/my_segment.py -f $TMP_DIR.data.filter/data.data.tgt.encode.valid -lan en
# keep valid src
cp $TMP_DIR.data.filter/data.data.origin.valid $TMP_DIR.data/data.valid
# move to gen
mkdir $TMP_DIR.gen/medicine -p
cp $TMP_DIR.data.filter/data.data.src.encode.train.seg $TMP_DIR.gen/medicine/train.zh
cp $TMP_DIR.data.filter/data.data.src.encode.valid.seg $TMP_DIR.gen/medicine/valid.zh
cp $TMP_DIR.data.filter/data.data.tgt.encode.train.seg $TMP_DIR.gen/medicine/train.en
cp $TMP_DIR.data.filter/data.data.tgt.encode.valid.seg $TMP_DIR.gen/medicine/valid.en
# tar
cd $TMP_DIR.gen
tar -cvf medicine.tar.gz medicine/train.en medicine/train.zh medicine/valid.en medicine/valid.zh

# t2t data gen
cd $CODE_DIR
python tensor2tensor/bin/t2t_datagen.py \
    --data_dir=$TMP_DIR/../t2t_datagen/new_med \
    --tmp_dir=$TMP_DIR.gen \
    --problem=translate_zhen_med_small_vocab \
    --t2t_usr_dir=$CODE_DIR/mytrain/my_t2t
