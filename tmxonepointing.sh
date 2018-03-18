#!/usr/bin/env bash

TASK=med_test/test/gen
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=test

# unpack if necessary
#python unpack.py -f $TMP_DIR/$FILE_NAME

# term encode, input: .zh output: .zh.decode .zh.decode.dict
python analyzerencode.py -f $TMP_DIR/$FILE_NAME.zh --report 100000
python analyzerencode.py -f $TMP_DIR/$FILE_NAME.en --report 100000

# segment, input: .en(zh).decode output: seg..en(zh).decode
python segment.py -f $TMP_DIR/$FILE_NAME.en.decode -l en
python segment.py -f $TMP_DIR/$FILE_NAME.zh.decode -l zh

# ==============================================
# decoder, problem, model and hparams
# ==============================================
PROBLEM=translate_zhen_new_med_small_vocab
MODEL=transformer
HPARAMS=transformer_big_single_gpu_batch_size

DATA_DIR=$HOMEPATH/t2t_data/new_medicine_all                                    # vocab
TRAIN_DIR=$HOMEPATH/t2t_train/new_medicine_all/$PROBLEM/$MODEL-$HPARAMS         # train model

# Decode
DECODE_FILE=$TMP_DIR/seg.$FILE_NAME.zh.decode
OUTPUT_FILE=$TMP_DIR/seg.$FILE_NAME.en.decode.translation

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

# Evaluate the BLEU score
# Note: Report this BLEU score in papers, not the internal approx_bleu metric.
python mybleu.py -rf $TMP_DIR/seg.$FILE_NAME.en.decode \
                 -tf $OUTPUT_FILE \
                 -l en --lower True
# ==============================================
# end decoder
# ==============================================

# term decode,
# input: .decode.en.translation, .decode.zh.dict,
# output: encode.seg..decode.en.translation
python analyzerdecode.py -f $TMP_DIR/seg.$FILE_NAME.en.decode.translation \
                         -d $TMP_DIR/$FILE_NAME.zh.decode.dict \
                         -t $TMP_DIR/encode.seg.$FILE_NAME.en.decode.translation \
                         --dict_type json

# just segment and cal bleu
## TODO: generate $FILE_NAME.en.translation with a python script: merge.py(unsegment)
#cp $TMP_DIR/encode.seg.$FILE_NAME.en.decode.translation $TMP_DIR/$FILE_NAME.en.translation
#
## segment to cal bleu
#python segment.py -f $TMP_DIR/$FILE_NAME.en -l en
#python segment.py -f $TMP_DIR/$FILE_NAME.en.translation -l en
#
#python mybleu.py -rf $TMP_DIR/seg.$FILE_NAME.en.decode \
#                 -tf $TMP_DIR/seg.$FILE_NAME.en.decode.translation \
#                 -l en --lower True --truncate 1000

# encode and cal bleu
python analyzerdecode.py -f $TMP_DIR/seg.$FILE_NAME.en.decode \
                         -d $TMP_DIR/$FILE_NAME.en.decode.dict \
                         -t $TMP_DIR/encode.seg.$FILE_NAME.en.decode \
                         --dict_type json

python mybleu.py -rf $TMP_DIR/encode.seg.$FILE_NAME.en.decode \
                 -tf $TMP_DIR/encode.seg.$FILE_NAME.en.decode.translation \
                 -l en --lower True --truncate 1000
