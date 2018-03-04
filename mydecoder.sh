#!/usr/bin/env bash

HOMEPATH=/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449/t2t_med

PROBLEM=translate_zhen_med_small_vocab
MODEL=transformer
HPARAMS=transformer_big_single_gpu_batch_size_2048

TMP_DIR=$HOMEPATH/t2t_datagen/medicine
DATA_DIR=$HOMEPATH/t2t_data/medicine
TRAIN_DIR=$HOMEPATH/t2t_train/medicine/$PROBLEM/$MODEL-$HPARAMS

# Decode
DECODE_FILE=$TMP_DIR/med_zhen_30000k_tok_dev.lang1
OUTPUT_FILE=$TRAIN_DIR/translation.en

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
TGT_FILE=$OUTPUT_FILE
python mybleu.py -rf $REF_FILE -tf $TGT_FILE -l en
