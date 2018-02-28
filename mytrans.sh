#!/usr/bin/env bash

python tensor2tensor/bin/t2t_trainer.py --registry_help

HOMEPATH=../t2t_med

PROBLEM=translate_enzh_med
MODEL=transformer
HPARAMS=transformer_base_single_gpu

TMP_DIR=$HOMEPATH/t2t_datagen/medicine
DATA_DIR=$HOMEPATH/t2t_data/medicine
TRAIN_DIR=$HOMEPATH/t2t_train/medicine/$PROBLEM/$MODEL-$HPARAMS

mkdir -p $DATA_DIR $TMP_DIR $TRAIN_DIR

# "Generate data"
python tensor2tensor/bin/t2t_datagen.py --data_dir=$DATA_DIR --tmp_dir=$TMP_DIR --problem=$PROBLEM

# echo "Train,* If you run out of memory, add --hparams='batch_size=1024'."
t2t-trainer --data_dir=$DATA_DIR --problems=$PROBLEM --model=$MODEL --hparams_set=$HPARAMS --output_dir=$TRAIN_DIR \
            --

# Decode

DECODE_FILE=$DATA_DIR/decode_this.txt
echo "Hello world" >> $DECODE_FILE
echo "Goodbye world" >> $DECODE_FILE
echo -e 'Hallo Welt\nAuf Wiedersehen Welt' > ref-translation.de

BEAM_SIZE=4
ALPHA=0.6

t2t-decoder \
  --data_dir=$DATA_DIR \
  --problems=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
  --decode_from_file=$DECODE_FILE \
  --decode_to_file=translation.en

# See the translations
cat translation.en

# Evaluate the BLEU score
# Note: Report this BLEU score in papers, not the internal approx_bleu metric.
t2t-bleu --translation=translation.en --reference=ref-translation.de