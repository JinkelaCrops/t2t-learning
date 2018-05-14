#!/usr/bin/env bash

export PYTHONPATH="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2:$PYTHONPATH"

# python tensor2tensor/bin/t2t_trainer.py --registry_help

PROBLEM=translate_enzh_new_med_small_vocab
MODEL=transformer
HPARAMS=transformer_big_single_gpu_batch_size_dropout_02
# MODEL=lstm_seq2seq_attention
# HPARAMS=lstm_luong_attention_larger_batch_size_2048

TMP_DIR=$HOMEPATH/t2t_datagen/new_medicine_new
DATA_DIR=$HOMEPATH/t2t_data/new_medicine_new
TRAIN_DIR=$HOMEPATH/t2t_train/new_medicine_new/$PROBLEM/$MODEL-$HPARAMS

mkdir -p $DATA_DIR $TMP_DIR $TRAIN_DIR

# echo "Train,* If you run out of memory, add --hparams='batch_size=1024'."
python tensor2tensor/bin/t2t_trainer.py \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --output_dir=$TRAIN_DIR \
    --gpuid=0,1 \
    --worker_gpu=2 \
    --train_steps=250000


