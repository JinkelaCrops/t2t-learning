#!/usr/bin/env bash

# python tensor2tensor/bin/t2t_trainer.py --registry_help

PROBLEM=translate_zhen_new_med_small_vocab
TMP_DIR=$HOMEPATH/t2t_datagen/med
DATA_DIR=$HOMEPATH/t2t_data/med

mkdir -p $DATA_DIR $TMP_DIR

# "Generate data"
python tensor2tensor/bin/t2t_datagen.py \
    --data_dir=$DATA_DIR \
    --tmp_dir=$TMP_DIR \
    --problem=$PROBLEM