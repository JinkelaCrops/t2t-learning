#!/usr/bin/env bash

TASK=tmxmall_med
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=Tmxmall医学语料_en-US_zh-CN_zh-CN_en-US.txt

# decoder
PROBLEM=translate_zhen_med
MODEL=transformer
HPARAMS=transformer_base_single_gpu_batch_size_4096

DATA_DIR=$HOMEPATH/t2t_data/medicine
TRAIN_DIR=$HOMEPATH/t2t_train/medicine/$PROBLEM/$MODEL-$HPARAMS

# Decode
DECODE_FILE=$TMP_DIR/seg.$FILE_NAME.zh
OUTPUT_FILE=$TMP_DIR/translation.en

BEAM_SIZE=4
ALPHA=0.6

python tensor2tensor/bin/t2t_decoder.py \
  --data_dir=$DATA_DIR \
  --problems=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
  --decode_from_file=$DECODE_FILE \
  --decode_to_file=$OUTPUT_FILE \
  --gpuid=0
#    FLAGS.decode_shards = 1
#    FLAGS.decode_interactive = False

# See the translations
head -1 $OUTPUT_FILE

# Evaluate the BLEU score
# Note: Report this BLEU score in papers, not the internal approx_bleu metric.
REF_FILE=$TMP_DIR/seg.$FILE_NAME.en
TGT_FILE=$OUTPUT_FILE
python mybleu.py -rf $REF_FILE -tf $TGT_FILE -l en --lower True
