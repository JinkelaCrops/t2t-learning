from nltk.translate.bleu_score import corpus_bleu
import re
import argparse

parser = argparse.ArgumentParser(description="mybleu.py")
parser.add_argument('-rf', "--ref_file_path")
parser.add_argument('-tf', "--tgt_file_path")
parser.add_argument('-l', "--language")

args = parser.parse_args()


class Decode(object):
    def __init__(self):
        pass

    @staticmethod
    def zh_separator(zh):
        return re.sub(" +", " ", re.sub("", " ", zh)).strip()

    @staticmethod
    def en_separator(en):
        return re.sub(" +", " ", en).strip()

    def zh_decode(self, path):
        with open(path, "r", encoding="utf8") as f:
            for line in f:
                yield self.zh_separator(line[:-1])

    def en_decode(self, path):
        with open(path, "r", encoding="utf8") as f:
            for line in f:
                yield self.en_separator(line[:-1])


if __name__ == '__main__':
    ref_path = args.ref_file_path
    tgt_path = args.tgt_file_path
    language = args.language

    decode = Decode()
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
# 0.32275, translate_zhen_med, opennmt baseline

# , translate_zhen_med, lstm_seq2seq_attention, lstm_luong_attention_larger_batch_size_2048

