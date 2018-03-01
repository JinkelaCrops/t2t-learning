#!/usr/bin/env bash

# python tensor2tensor/bin/t2t_trainer.py --registry_help

HOMEPATH=../t2t_med

PROBLEM=translate_enzh_med
MODEL=transformer
HPARAMS=transformer_base_single_gpu
# MODEL=lstm_seq2seq_attention
# HPARAMS=lstm_luong_attention_multi

TMP_DIR=$HOMEPATH/t2t_datagen/medicine
DATA_DIR=$HOMEPATH/t2t_data/medicine
TRAIN_DIR=$HOMEPATH/t2t_train/medicine/$PROBLEM/$MODEL-$HPARAMS

mkdir -p $DATA_DIR $TMP_DIR $TRAIN_DIR

# echo "Train,* If you run out of memory, add --hparams='batch_size=1024'."
python tensor2tensor/bin/t2t_trainer.py \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --output_dir=$TRAIN_DIR \
    --gpuid=0

