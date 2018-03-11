#!/usr/bin/env bash

PROBLEM=translate_zhen_new_med_small_vocab
#MODEL=lstm_seq2seq_attention
#HPARAMS=lstm_luong_attention_multi_larger_batch_size_2048
MODEL=transformer
HPARAMS=transformer_big_single_gpu_batch_size_1024

TMP_DIR=$HOMEPATH/t2t_datagen/new_medicine
DATA_DIR=$HOMEPATH/t2t_data/new_medicine
TRAIN_DIR=$HOMEPATH/t2t_train/new_medicine/$PROBLEM/$MODEL-$HPARAMS

# Decode
#DECODE_FILE=$TMP_DIR/med_zhen_30000k_tok_dev.lang1
DECODE_FILE=$HOMEPATH/t2t_datagen/med_test/valid2/seg.valid2.zh.decode
OUTPUT_FILE=$TRAIN_DIR/valid2.t2t_transformer_big_bpe.new

BEAM_SIZE=4
ALPHA=0.6
BATCH_SIZE=32

python tensor2tensor/bin/t2t_decoder.py \
  --data_dir=$DATA_DIR \
  --problems=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA,batch_size=$BATCH_SIZE" \
  --decode_from_file=$DECODE_FILE \
  --decode_to_file=$OUTPUT_FILE \
  --gpuid=0
#    FLAGS.decode_shards = 1
#    FLAGS.decode_interactive = False

# See the translations
head -1 $OUTPUT_FILE

# Evaluate the BLEU score
# Note: Report this BLEU score in papers, not the internal approx_bleu metric.
#REF_FILE=$TMP_DIR/med_zhen_30000k_tok_dev.lang2
REF_FILE=$HOMEPATH/t2t_datagen/med_test/valid2/seg.valid2.en.decode
TGT_FILE=$OUTPUT_FILE
python mybleu.py -rf $REF_FILE -tf $TGT_FILE -l en

# encode and cal bleu
python analyzerdecode.py -f $OUTPUT_FILE \
                         -d $HOMEPATH/t2t_datagen/med_test/valid2/valid2.zh.decode.dict \
                         -t $OUTPUT_FILE.encode \
                         --dict_type json

python mybleu.py -rf $HOMEPATH/t2t_datagen/med_test/valid2/valid2.en \
                 -tf $OUTPUT_FILE.encode \
                 -l en --lower True --truncate 1000