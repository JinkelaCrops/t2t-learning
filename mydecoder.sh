#!/usr/bin/env bash

PROBLEM=translate_zhen_new_med_small_vocab
MODEL=transformer
HPARAMS=transformer_base_single_gpu_batch_size_4096

TMP_DIR=$HOMEPATH/t2t_datagen/new_medicine
DATA_DIR=$HOMEPATH/t2t_data/new_medicine
TRAIN_DIR=$HOMEPATH/t2t_train/new_medicine/$PROBLEM/$MODEL-$HPARAMS

# Decode
DECODE_FILE=$TMP_DIR/med_zhen_30000k_tok_dev.lang1
#DECODE_FILE=$HOMEPATH/t2t_datagen/med_test/seg.src.test.txt.zh
OUTPUT_FILE=$TRAIN_DIR/translation.en.test

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
head -10 $OUTPUT_FILE

# Evaluate the BLEU score
# Note: Report this BLEU score in papers, not the internal approx_bleu metric.
REF_FILE=$TMP_DIR/med_zhen_30000k_tok_dev.lang2
#REF_FILE=$HOMEPATH/t2t_datagen/med_test/seg.src.test.txt.en
TGT_FILE=$OUTPUT_FILE
python mybleu.py -rf $REF_FILE -tf $TGT_FILE -l en
