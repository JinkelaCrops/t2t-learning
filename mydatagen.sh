#!/usr/bin/env bash

# python tensor2tensor/bin/t2t_trainer.py --registry_help

HOMEPATH=../t2t_med

PROBLEM=translate_zhen_med_small_vocab
TMP_DIR=$HOMEPATH/t2t_datagen/medicine
DATA_DIR=$HOMEPATH/t2t_data/medicine

mkdir -p $DATA_DIR $TMP_DIR

# "Generate data"
python tensor2tensor/bin/t2t_datagen.py \
    --data_dir=$DATA_DIR \
    --tmp_dir=$TMP_DIR \
    --problem=$PROBLEM