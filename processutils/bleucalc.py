from nltk.translate.bleu_score import corpus_bleu
import re


class BleuDecorate(object):
    def __init__(self, lower=False, truncate=1E10):
        self.lower = lower
        if self.lower:
            self.conv = lambda x: x.lower()
        else:
            self.conv = lambda x: x
        self.truncate = truncate
        pass

    @staticmethod
    def zh_separator(zh):
        return re.sub(" +", " ", re.sub("(?<=[\\u4e00-\\u9fff])(?=[\\u4e00-\\u9fff])", " ", zh)).strip()

    @staticmethod
    def en_separator(en):
        return re.sub(" +", " ", en).strip()

    def zh_decorate(self, data):
        for k, line in enumerate(data):
            if k < self.truncate:
                yield self.zh_separator(self.conv(line.strip()))

    def en_decorate(self, data):
        for k, line in enumerate(data):
            if k < self.truncate:
                yield self.en_separator(self.conv(line.strip()))


def bleu_calc(ref_lines, tgt_lines, language, lower=True, truncate=1E10):
    decorate = BleuDecorate(lower, truncate)
    if language == "zh":
        ref = [line.split() for line in decorate.zh_decorate(ref_lines)]
        tgt = [line.split() for line in decorate.zh_decorate(tgt_lines)]
    else:
        ref = [line.split() for line in decorate.en_decorate(ref_lines)]
        tgt = [line.split() for line in decorate.en_decorate(tgt_lines)]

    return corpus_bleu([[r] for r in ref], tgt)
