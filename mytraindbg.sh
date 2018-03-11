#!/usr/bin/env bash

PROBLEM=translate_zhen_new_med_simple
MODEL=transformer
HPARAMS=transformer_base_single_gpu_batch_size_4096

DATA_DIR=$HOMEPATH/t2t_data/new_medicine
TRAIN_DIR=$HOMEPATH/t2t_train/new_medicine/$PROBLEM/$MODEL-$HPARAMS

mkdir -p $DATA_DIR $TRAIN_DIR

# echo "Train,* If you run out of memory, add --hparams='batch_size=1024'."
python tensor2tensor/bin/t2t_trainer.py \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --output_dir=$TRAIN_DIR \
    --gpuid=0 \
    --worker_gpu=1 \
    --train_steps=200 \
    --tfdbg=True