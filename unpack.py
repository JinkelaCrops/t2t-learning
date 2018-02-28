import re
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="unpack.py")

parser.add_argument('-f', "--file_path")
parser.add_argument('-s', "--separator")

args = parser.parse_args()


class Base(object):
    def __init__(self):
        pass

    def zhratio(self, sentence):
        ratio = len(re.findall("[\u4000-\u9FFF]", sentence)) / len(sentence)
        return ratio

    def regratio(self, reg, sentence):
        ratio = len(re.findall(reg, sentence)) / len(sentence)
        return ratio

    def simple_zhen_ratio(self, sen):
        zhr = len(re.findall("[\u4000-\u9fff]", sen)) / len(sen)
        enr = len(re.findall("[A-z]", sen)) / len(sen)
        ratio = zhr * enr
        return ratio


class Sepautosplit(Base):

    def __init__(self, sep):
        self.sep = sep
        self.bisentence = ""

    def compare_bisentence(self):
        self.comparedf = pd.DataFrame()

        seplist = self.bisentence.split(self.sep)
        tmp = [[self.sep.join(seplist[:i]).strip(), self.sep.join(seplist[i:]).strip()] for i in range(1, len(seplist))]
        self.comparedf["lines"] = list(filter(lambda x: len(x[0]) * len(x[1]) > 0, tmp))
        self.comparedf["linesee"] = self.comparedf["lines"].apply(
            lambda sen: [re.sub("[\u4000-\u9fff]", "ee", x) for x in sen])
        self.comparedf["lendiff"] = self.comparedf["linesee"].apply(
            lambda sen: abs(len(sen[0]) - len(sen[1])) / max(len(sen[0]), len(sen[1])))
        self.comparedf["zhratiozero"] = self.comparedf["lines"].apply(
            lambda sen: self.simple_zhen_ratio(sen[0]) + self.simple_zhen_ratio(sen[1]))
        self.comparedf["samepartratio"] = self.comparedf["lines"].apply(
            lambda sen: self.headend_soft_ratio(*sen, 10, 10) / 2)

    def sep_auto_detect(self, bisentence, verbose=False):
        self.bisentence = bisentence
        self.compare_bisentence()
        # lendiff最小的3个为候选
        candidatedf = self.comparedf.sort_values(by="lendiff")[:3]
        # 候选句子zhratiozero, 首尾samepart, lendiff比例排序
        # mean, score越小越好
        candidatedf["score"] = candidatedf[["samepartratio", "zhratiozero", "lendiff"]].mean(axis=1)
        self.zh_sentense, self.en_sentence = candidatedf.sort_values(by="score")["lines"].iloc[0]
        if verbose:
            print("###", self.zh_sentense)
            print("###", self.en_sentence)
        return self.zh_sentense, self.en_sentence


class Unpack(Base):
    def __init__(self, sep):
        self.sep = sep
        self.bisentence = ""
        self.auto = Sepautosplit(sep)

    def whichzh(self, zh, en):
        if self.zhratio(zh) < self.zhratio(en):
            return en, zh, True
        else:
            return zh, en, False

    def unpack(self, bisentence):

        self.bisentence = bisentence[:-1]  # get rid of \n
        if len(re.findall("\u0000", self.bisentence.replace(self.sep, "\u0000"))) > 1:
            zh, en = self.auto.sep_auto_detect(self.bisentence)
        else:
            zh, en = self.bisentence.split(self.sep)
        zh, en, change_order = self.whichzh(zh, en)
        return zh, en, change_order


if __name__ == "__main__":
    sep = args.separator
    file_path = args.file_path
    file_name = file_path.replace("\\","/").split("/")[-1]

    unpack = Unpack(sep)
    print(f"unpack info: unpacking file with separator '{sep}'")
    zh_lines = []
    en_lines = []
    with open(file_path, "r", encoding="utf8") as f:
        for line in f:
            try:
                zh, en, change_order = unpack.unpack(line.strip())
                zh_lines.append(zh)
                en_lines.append(en)
            except Exception as e:
                print(f"unpack error: {e.__context__}, ### {line.strip()}")
                pass

    print(f"unpack info: export to {file_name}.zh and {file_name}.en")
    with open(file_path + ".zh", "w", encoding="utf8") as f:
        f.writelines(["%s\n" % zh for zh in zh_lines])
    with open(file_path + ".en", "w", encoding="utf8") as f:
        f.writelines(["%s\n" % en for en in en_lines])
