#!/usr/bin/env bash

# python tensor2tensor/bin/t2t_trainer.py --registry_help

export PYTHONPATH="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2:$PYTHONPATH"
CODE_DIR="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2"
TMP_DIR="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2/test/medicine.sample"
#export PYTHONPATH="/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2:$PYTHONPATH"
#CODE_DIR="/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2"
#TMP_DIR="/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2/test/medicine.sample"

PROBLEM=translate_zhen_med_small_vocab
MODEL=transformer
HPARAMS=transformer_big_single_gpu_batch_size_1600

DATA_DIR=$TMP_DIR/../t2t_datagen/new_med
TRAIN_DIR=$TMP_DIR/../t2t_train/new_med/$PROBLEM/$MODEL-$HPARAMS

mkdir -p $TRAIN_DIR
cd $CODE_DIR
python tensor2tensor/bin/t2t_trainer.py \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --output_dir=$TRAIN_DIR \
    --worker_gpu=1 \
    --train_steps=1000

