import re
import pandas as pd
import random
from difflib import SequenceMatcher


class Base(object):
    def __init__(self):
        pass

    @staticmethod
    def zhratio(sentence):
        ratio = len(re.findall("[\\u4000-\\u9FFF]", sentence)) / len(sentence)
        return ratio

    @staticmethod
    def regratio(reg, sentence):
        ratio = len(re.findall(reg, sentence)) / len(sentence)
        return ratio

    @staticmethod
    def simple_zhen_ratio(sen):
        zhr = len(re.findall("[\\u4000-\\u9fff]", sen)) / len(sen)
        enr = len(re.findall("[A-Za-z]", sen)) / len(sen)
        ratio = zhr * enr
        return ratio

    @staticmethod
    def headend_hard_ratio(zhsen, ensen, headn, endn):
        def part_dict(sen, allpart=False):
            n = len(sen)
            if allpart:
                part = [sen[i:j] for i in range(n) for j in range(i + 1, n + 1)]
            else:
                part = [sen[:i] for i in range(1, n + 1)]
            return part

        def samepart_ratio(zhpart, enpart):
            tmp = [x == y for x in zhpart for y in enpart]
            return sum(tmp) / len(tmp)

        headratio = samepart_ratio(part_dict(zhsen[:headn]), part_dict(ensen[:headn]))
        endratio = samepart_ratio(part_dict(zhsen[-endn:][::-1]), part_dict(ensen[-endn:][::-1]))
        return 2 - headratio - endratio

    @staticmethod
    def headend_soft_ratio(zhsen, ensen, headn, endn):
        def part_dict(sen, allpart=False):
            n = len(sen)
            if allpart:
                part = [sen[i:j] for i in range(n) for j in range(i + 1, n + 1)]
            else:
                part = [sen[:i] for i in range(1, n + 1)]
            return part

        def samepart_ratio(zhpart, enpart):
            tmp = [SequenceMatcher(None, x, y).ratio() for x in zhpart for y in enpart]
            return max(tmp)

        headratio = samepart_ratio(part_dict(zhsen[:headn]), part_dict(ensen[:headn]))
        endratio = samepart_ratio(part_dict(zhsen[-endn:][::-1]), part_dict(ensen[-endn:][::-1]))
        return 2 - headratio - endratio


class Sepautosplit(Base):
    def __init__(self, sep):
        super(Sepautosplit, self).__init__()
        self.sep = sep
        self.bisentence = ""
        self.zh_sentense = ""
        self.en_sentence = ""
        self.comparedf = None

    def compare_bisentence(self):
        self.comparedf = pd.DataFrame()

        seplist = self.bisentence.split(self.sep)
        tmp = [[self.sep.join(seplist[:i]).strip(), self.sep.join(seplist[i:]).strip()] for i in range(1, len(seplist))]
        self.comparedf["lines"] = list(filter(lambda x: len(x[0]) * len(x[1]) > 0, tmp))
        self.comparedf["linesee"] = self.comparedf["lines"].apply(
            lambda sen: [re.sub("[\\u4000-\\u9fff]", "ee", x) for x in sen])
        self.comparedf["lendiff"] = self.comparedf["linesee"].apply(
            lambda sen: abs(len(sen[0]) - len(sen[1])) / max(len(sen[0]), len(sen[1])))
        self.comparedf["zhratiozero"] = self.comparedf["lines"].apply(
            lambda sen: self.simple_zhen_ratio(sen[0]) + self.simple_zhen_ratio(sen[1]))
        self.comparedf["samepartratio"] = self.comparedf["lines"].apply(
            lambda sen: self.headend_soft_ratio(*sen, 10, 10) / 2)

    def sep_auto_detect(self, bisentence):
        self.bisentence = bisentence
        self.compare_bisentence()
        # lendiff最小的3个为候选
        candidatedf = self.comparedf.sort_values(by="lendiff")[:3]
        # 候选句子zhratiozero, 首尾samepart, lendiff比例排序
        # mean, score越小越好
        candidatedf["score"] = candidatedf[["samepartratio", "zhratiozero", "lendiff"]].mean(axis=1)
        self.zh_sentense, self.en_sentence = candidatedf.sort_values(by="score")["lines"].iloc[0]
        return self.zh_sentense, self.en_sentence


class Unpack(Base):
    def __init__(self, sep):
        super(Unpack, self).__init__()
        self.sep = sep
        self.bisentence = ""
        self.auto = Sepautosplit(sep)

    def whichzh(self, zh, en):
        if self.zhratio(zh) < self.zhratio(en):
            return en, zh, True
        else:
            return zh, en, False

    def unpack(self, bisentence):
        self.bisentence = bisentence.strip("\n")  # get rid of \n
        if len(re.findall("\\u0000", self.bisentence.replace(self.sep, "\u0000"))) > 1:
            zh, en = self.auto.sep_auto_detect(self.bisentence)
        else:
            zh, en = self.bisentence.split(self.sep)
        zh, en, change_order = self.whichzh(zh, en)
        return zh, en, change_order


class DataSplit(object):
    def __init__(self):
        pass

    @staticmethod
    def train_valid_split(lines, size=None, shuffle=True):
        size = min(int(len(lines) * 0.1), 10000) if size is None else size
        if shuffle:
            random.seed(0)
            lines = random.sample(lines, len(lines))
        return lines[:-size], lines[-size:]

    @staticmethod
    def train_valid_test_split(lines, size=None, shuffle=True):
        size = min(int(len(lines) * 0.1), 10000) if size is None else size
        if shuffle:
            random.seed(0)
            lines = random.sample(lines, len(lines))
        return lines[:-2 * size], lines[-2 * size:-size], lines[-size:]


class BiRawFilter(object):
    def __init__(self, sep, new_sep):
        self.sep = sep
        self.new_sep = new_sep

    def replace_bad_sep(self, bisentence):
        bisentence = bisentence.replace(self.new_sep, "").replace(self.sep, self.new_sep)
        return bisentence

    def tridots_filter(self, bisentence):
        """
        filter tridots such as ...
        """
        return re.search("\.\.\. *$", bisentence) is not None

    def simple_filter(self, bisentence):
        """
        simple, only have A-Za-z \u4e00-\u9fff ,. ，。in sentence
        """
        return re.search("[^A-Za-z\\u4e00-\\u9fff %s\n\.,。，]" % self.new_sep, bisentence) is not None

    def clear_filter(self, bisentence):
        """
        clear, have \u4e00-\u9fff in only one side
        """
        return re.search("[\\u4e00-\\u9fff].*%s.*[\\u4e00-\\u9fff]" % self.new_sep, bisentence) is not None

    def line_filter(self, bisentence):
        bisentence = self.replace_bad_sep(bisentence).strip()
        flag = self.tridots_filter(bisentence) or self.simple_filter(bisentence) or self.clear_filter(bisentence)
        return flag

    def filter(self, lines):
        return [line for line in lines if not self.line_filter(line)]


class RawFilter(object):
    def __init__(self):
        pass

    @staticmethod
    def tridots_filter(zh, en):
        """
        filter tridots such as ...
        """
        regex = "\.\.\. *$"
        return re.search(regex, zh) is not None or re.search(regex, en) is not None

    @staticmethod
    def simple_filter(zh, en):
        """
        simple, only have A-Za-z \u4e00-\u9fff ,. ，。in sentence
        """
        regex = "[^A-Za-z\\u4e00-\\u9fff \.,。，]"
        return re.search(regex, zh) is not None or re.search(regex, en) is not None

    @staticmethod
    def clear_filter(zh, en):
        """
        clear, have \u4e00-\u9fff in only one side
        """
        regex = "[\\u4e00-\\u9fff].*\\u0000.*[\\u4e00-\\u9fff]"
        return re.search(regex, zh + "\u0000" + en) is not None

    def line_filter(self, zh, en):
        flag = self.tridots_filter(zh, en) or self.simple_filter(zh, en) or self.clear_filter(zh, en)
        return flag

    def filter(self, zh_lines, en_lines):
        filter_output = [(zh, en) for zh, en in zip(zh_lines, en_lines) if not self.line_filter(zh, en)]
        return [x[0] for x in filter_output], [x[1] for x in filter_output]
