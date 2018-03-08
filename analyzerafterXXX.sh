#!/usr/bin/env bash

PROBLEM=translate_zhen_new_med_small_vocab
MODEL=transformer
HPARAMS=transformer_base_single_gpu_batch_size_4096

TMP_DIR=$HOMEPATH/t2t_datagen/new_medicine
DATA_DIR=$HOMEPATH/t2t_data/new_medicine
TRAIN_DIR=$HOMEPATH/t2t_train/new_medicine/$PROBLEM/$MODEL-$HPARAMS

# Decode
#DECODE_FILE=$TMP_DIR/med_zhen_30000k_tok_dev.lang1
DECODE_FILE=$HOMEPATH/t2t_datagen/med_test/seg.src.test.txt.decode.zh
OUTPUT_FILE=$TRAIN_DIR/translation.en.test.srctest

#REF_FILE=$TMP_DIR/med_zhen_30000k_tok_dev.lang2
REF_FILE=$HOMEPATH/t2t_datagen/med_test/seg.src.test.txt.decode.en
TGT_FILE=$OUTPUT_FILE

python analyzerdecode.py -f $OUTPUT_FILE -d $HOMEPATH/t2t_datagen/med_test/src.test.txt.decode.dict -t $TRAIN_DIR/translation.en.srctest
python mybleu.py -rf $HOMEPATH/t2t_datagen/med_test/seg.encode.src.test.txt.decode.en -tf $TRAIN_DIR/translation.en.srctest -l en --lower True
