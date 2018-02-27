from nltk.translate.bleu_score import corpus_bleu
import re

path = "/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2/tensor2tensor"

problems = "translate_enzh_med"
model = "transformer"
hparams_set = "transformer_base_single_gpu"
# model = "lstm_seq2seq_attention"
# hparams_set = "lstm_luong_attention_multi"
output_dir = f"{path}/train/{problems}/{model}-{hparams_set}"
ref_path = f"{path}/tmp/t2t_datagen/med_enzh_50000k_tok_dev.lang2"
tgt_path = f"{output_dir}/translation.zh"


def split_every(path):
    with open(path, "r", encoding="utf8") as f:
        data = f.readlines()

    def decode(line):
        return re.sub(" +", " ", re.sub("", " ", line)).strip()

    data = [decode(x[:-1]) for x in data]
    return data


ref = [line.split() for line in split_every(ref_path)]
tgt = [line.split() for line in split_every(tgt_path)]



corpus_bleu([[r] for r in ref], tgt)
# 0.17842, translate_enzh_wmt8k, transformer, transformer_base_single_gpu
# 0.09039, translate_enzh_wmt8k, lstm_seq2seq_attention, lstm_luong_attention_multi

"""
from tensor2tensor.utils import bleu_hook
import tensorflow as tf
flags = tf.flags
FLAGS = flags.FLAGS
path = "/media/yanpan/7D4CF1590195F939/Projects/tensor2tensor-1.4.2/tensor2tensor"
FLAGS.reference = f"{path}/tmp/t2t_datagen/wmt_enzh_8192k_tok_dev.lang2"
FLAGS.translation = f"{path}/tmp/t2t_datagen/translation.zh"

bleu_hook.bleu_wrapper(FLAGS.reference, FLAGS.translation, case_sensitive=True)
"""
