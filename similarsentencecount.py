from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.bleu_score import sentence_bleu
import numpy as np
import re
import argparse

parser = argparse.ArgumentParser(description="similarsentencecount.py")
parser.add_argument('-rf', "--ref_file_path")
parser.add_argument('-tf', "--tgt_file_path")
parser.add_argument('-l', "--language")
parser.add_argument("--lower", default=False, type=bool)
parser.add_argument("--truncate", default=1E10, type=int)

args = parser.parse_args()


class Decode(object):
    def __init__(self, lower=False, truncate=1E10):
        self.lower = lower
        self.truncate = truncate
        pass

    @staticmethod
    def zh_separator(zh):
        return re.sub(" +", " ", re.sub("", " ", zh)).strip()

    @staticmethod
    def en_separator(en):
        return re.sub(" +", " ", en).strip()

    def zh_decode(self, path):
        if self.lower:
            with open(path, "r", encoding="utf8") as f:
                for k, line in enumerate(f):
                    if k < self.truncate:
                        yield self.zh_separator(line[:-1].lower())
        else:
            with open(path, "r", encoding="utf8") as f:
                for k, line in enumerate(f):
                    if k < self.truncate:
                        yield self.zh_separator(line[:-1])

    def en_decode(self, path):
        if self.lower:
            with open(path, "r", encoding="utf8") as f:
                for k, line in enumerate(f):
                    if k < self.truncate:
                        yield self.en_separator(line[:-1].lower())
        else:
            with open(path, "r", encoding="utf8") as f:
                for k, line in enumerate(f):
                    if k < self.truncate:
                        yield self.en_separator(line[:-1])


if __name__ == '__main__':
    ref_path = args.ref_file_path
    tgt_path = args.tgt_file_path
    language = args.language

    decode = Decode(args.lower, args.truncate)
    func = decode.zh_decode if language == "zh" else decode.en_decode
    file_bleus = []
    with open(tgt_path, "r", encoding="utf8") as ff:
        tf_length = len(ff.readlines())

    f = open(args.tgt_file_path + ".compare_bleu", "w", encoding="utf8")
    for k, tf_line in enumerate(func(tgt_path)):
        tf_compare_bleu = [sentence_bleu([rf_line], tf_line) for rf_line in func(ref_path)]
        max_tf_compare_bleu = max(tf_compare_bleu)
        file_bleus.append(max_tf_compare_bleu)
        f.writelines("%s\n" % max_tf_compare_bleu)
        print("processing %s" % (k+1))

    f.close()
    print("potential 95 percent same %s " % (np.sum(np.array(file_bleus) > 0.95) / tf_length))
    print("potential 90 percent same %s " % (np.sum(np.array(file_bleus) > 0.90) / tf_length))
    print("potential 80 percent same %s " % (np.sum(np.array(file_bleus) > 0.80) / tf_length))
    print("potential 70 percent same %s " % (np.sum(np.array(file_bleus) > 0.70) / tf_length))
    print("potential 60 percent same %s " % (np.sum(np.array(file_bleus) > 0.60) / tf_length))

# 0.17842, translate_enzh_wmt8k, transformer, transformer_base_single_gpu
# 0.09039, translate_enzh_wmt8k, lstm_seq2seq_attention, lstm_luong_attention_multi
# 0.40956, translate_enzh_med, transformer, transformer_base_single_gpu
# 0.28273, translate_zhen_med, transformer, transformer_base_single_gpu
# 0.22729, translate_zhen_med, lstm_seq2seq_attention, lstm_luong_attention_batch_size_2048
# 0.32275, translate_zhen_med, opennmt baseline


# 0.31475, translate_zhen_med, transformer, transformer_base_single_gpu_batch_size_4096, 2 gpus
# 0.27262, translate_zhen_med, transformer, transformer_base_single_gpu_batch_size_2048, 2 gpus
# 0.25179, translate_zhen_med, transformer, transformer_base_single_gpu_batch_size_1024, 2 gpus

# 0.26694, translate_zhen_med_small_vocab, transformer, transformer_big_batch_size_2048, 2 gpus
# 0.40032, translate_zhen_med_small_vocab, transformer, transformer_big_single_gpu_batch_size_2048, 2 gpus
# 0.30513, translate_zhen_med_small_vocab, transformer, transformer_big_single_gpu_batch_size_2048_warmup_24000, 2 gpus
# 0.32834, translate_zhen_med_small_vocab, transformer, transformer_base_single_gpu_batch_size_4096, 2 gpus
