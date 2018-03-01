#!/usr/bin/env bash

# python tensor2tensor/bin/t2t_trainer.py --registry_help

HOMEPATH=/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449/t2t_med

PROBLEM=translate_zhen_med_simple
TMP_DIR=$HOMEPATH/t2t_datagen/medicine
DATA_DIR=$HOMEPATH/t2t_data/medicine

mkdir -p $DATA_DIR $TMP_DIR

# "Generate data"
python tensor2tensor/bin/t2t_datagen.py \
    --data_dir=$DATA_DIR \
    --tmp_dir=$TMP_DIR \
    --problem=$PROBLEM