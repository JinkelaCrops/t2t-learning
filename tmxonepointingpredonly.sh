#!/usr/bin/env bash

TASK=tmxmall_med
TMP_DIR=$HOMEPATH/t2t_datagen/$TASK
FILE_NAME=Tmxmall医学语料_en-US_zh-CN_zh-CN_en-US.txt

cp $TMP_DIR/$FILE_NAME $TMP_DIR/$FILE_NAME.zh

# term encode, input: .zh output: .zh.decode .zh.decode.dict
python analyzerencode.py -f $TMP_DIR/$FILE_NAME.zh --report 100000

# segment, input: .en(zh).decode output: seg..en(zh).decode
python segment.py -f $TMP_DIR/$FILE_NAME.zh.decode -l zh

# ==============================================
# decoder, problem, model and hparams
# ==============================================
PROBLEM=translate_zhen_new_med_small_vocab
MODEL=transformer
HPARAMS=transformer_base_single_gpu_batch_size_4096

DATA_DIR=$HOMEPATH/t2t_data/new_medicine                                    # vocab
TRAIN_DIR=$HOMEPATH/t2t_train/new_medicine/$PROBLEM/$MODEL-$HPARAMS         # train model

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

# ==============================================
# end decoder
# ==============================================

# term decode,
# input: .decode.en.translation, .decode.zh.dict,
# output: encode.seg..decode.en.translation
python analyzerdecode.py -f $TMP_DIR/seg.$FILE_NAME.en.decode.translation \
                         -d $TMP_DIR/$FILE_NAME.zh.decode.dict \
                         -t $TMP_DIR/encode.seg.$FILE_NAME.en.decode.translation

# TODO: generate $FILE_NAME.en.translation with a python script: merge.py(unsegment)
cp $TMP_DIR/encode.seg.$FILE_NAME.en.decode.translation $TMP_DIR/$FILE_NAME.en.translation

