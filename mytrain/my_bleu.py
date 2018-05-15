from nltk.translate.bleu_score import corpus_bleu
import re
import argparse

parser = argparse.ArgumentParser(description="mybleu.py")
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
        return re.sub(" +", " ", re.sub("(?<=[\\u4e00-\\u9fff])(?=[\\u4e00-\\u9fff])", " ", zh)).strip()

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
    if language == "zh":
        ref = [line.split() for line in decode.zh_decode(ref_path)]
        tgt = [line.split() for line in decode.zh_decode(tgt_path)]
    else:
        ref = [line.split() for line in decode.en_decode(ref_path)]
        tgt = [line.split() for line in decode.en_decode(tgt_path)]

    print("my bleu: bleu4 is %s" % corpus_bleu([[r] for r in ref], tgt))

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
