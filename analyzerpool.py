import re
import numpy as np
from collections import OrderedDict


# import argparse
#
# parser = argparse.ArgumentParser(description="analyzerpool.py")
# parser.add_argument('-f', "--file_path_prefix")
#
# args = parser.parse_args()

class Token(object):
    def __init__(self):
        self.level_map = {}
        self.level_map = self.get_token_level

    @property
    def get_token_name(self):
        #  bad
        return ["PercentDecimal", "PercentInteger", "NumericDecimal", "NumericInteger", "NumericYear", "TermUpperCase",
                "TermCamelCase", "TermEnCharWithNum", "TermChemicalPrefix"]

    @property
    def get_token_level(self):
        if len(self.level_map) == 0:
            for token_name in self.get_token_name:
                token = getattr(self, token_name)
                token_level = token.level
                self.level_map[token_name] = token_level
                print(f"Token.get_level_map info: {token_name} has level {token_level}")
        return self.level_map

    def set_token_level(self, level_map_part):
        for token_name, token_level in level_map_part.items():
            self.level_map[token_name] = token_level
            print(f"Token.get_level_map info: reset {token_name} 's level to {token_level}")

    class PercentDecimal(object):
        level = 1

        @staticmethod
        def process(sent):
            """55.55%，必须是小数，允许空格"""
            targets = re.findall("[0-9][0-9 ]*\.[0-9 ]*[0-9] *%", sent)
            return sub_space(targets)

    class PercentInteger(object):
        level = 0.9

        @staticmethod
        def process(sent):
            """100%，必须是整数，允许空格"""
            targets = re.findall("[0-9][0-9 ]* *%", sent)
            return sub_space(targets)

    class NumericDecimal(object):
        level = 1

        @staticmethod
        def process(sent):
            """55.55"""
            targets = re.findall("[0-9][0-9 ]*\.[0-9 ]*[0-9]", sent)
            return sub_space(targets)

    class NumericInteger(object):
        level = 0

        @staticmethod
        def process(sent):
            """5"""
            targets = re.findall("[0-9][0-9 ]*[0-9]", sent)
            return sub_space(targets)

    class NumericYear(object):
        level = 0.9

        @staticmethod
        def process(sent):
            """2009"""
            targets = re.findall("1[5-9][0-9]{2}|20[0-1][0-9]", sent)
            return targets

    class TermUpperCase(object):
        level = 0.2

        @staticmethod
        def process(sent):
            """DNA"""
            targets = re.findall("\\b[A-Z]+\\b", sent)
            return targets

    class TermCamelCase(object):
        level = 0.1

        @staticmethod
        def process(sent):
            """pH，PubMed, LoL, but not DNA, ID"""
            # "\\b[A-Za-z]+[A-Z]+[a-z][A-Za-z]*\\b" # 词中大写
            # "\\b[A-Za-z]+[a-z][A-Z]+\\b"          # 词末大写
            targets = re.findall("\\b[A-Za-z]+[A-Z]+[A-Za-z]*\\b", sent)
            return targets

    class TermEnCharWithNum(object):
        level = 0.3

        @staticmethod
        def process(sent):
            """EP2"""
            targets = re.findall("\\b[0-9]+[A-Za-z]+[0-9A-Za-z]*\\b|\\b[0-9A-Za-z]+[A-Za-z]+[0-9]+\\b", sent)
            return targets

    class TermChemicalPrefix(object):
        level = 0.3
        """1,3,7-"""
        regex = "(?<![\w\-])([0-9]+ *[,，] *)*[0-9]+\-(?=[A-Za-z\u4000-\u9fff])"

        @classmethod
        def process(cls, sent):
            # TODO: SubwordTextEncoder, and the paper with group sub
            matcher = re.finditer(cls.regex, sent)
            subs = re.sub(cls.regex, cls.__name__, sent)
            targets = []
            pattern = OrderedDict()
            for k, m in enumerate(matcher):
                targets.append(m.group())
                pattern[(m.start(), m.end())] = cls.__name__ + f"_{k}"
            return sub_space(targets)


def sub_space(targets):
    return [re.sub(" ", "", target) for target in targets]


def execute_token(sent, tokens):
    return {token_name: getattr(tokens, token_name).process(sent) for token_name in tokens.get_token_name}


file_path_prefix = "../t2t_med/t2t_datagen/medicine/medicine.sample.big.txt"
zh_file_path = file_path_prefix + ".zh"
en_file_path = file_path_prefix + ".en"

tokens = Token()
zh_file_dict = {}
with open(zh_file_path, "r", encoding="utf8") as f:
    for k, line in enumerate(f):
        zh_file_dict[k] = execute_token(line[:-1], tokens)

en_file_dict = {}
with open(en_file_path, "r", encoding="utf8") as f:
    for k, line in enumerate(f):
        en_file_dict[k] = execute_token(line[:-1], tokens)


def flag_gen(i):
    if zh_file_dict[i] == en_file_dict[i]:
        if any(zh_file_dict[i].values()):
            return 2
        else:
            return 1
    else:
        return 0


ok_flag = [flag_gen(i) for i in range(len(zh_file_dict))]
print(np.mean(np.array(ok_flag) > 0))
print(np.mean(np.array(ok_flag) == 1))
print(np.mean(np.array(ok_flag) == 2))

nonempty_line = []
empty_line = []
f = open(zh_file_path, "r", encoding="utf8")
g = open(en_file_path, "r", encoding="utf8")
w0 = open(file_path_prefix + ".term_error", "w", encoding="utf8")
w1 = open(file_path_prefix + ".term_empty", "w", encoding="utf8")
w2 = open(file_path_prefix + ".term_nonempty", "w", encoding="utf8")

for k, (zh_line, en_line) in enumerate(zip(f, g)):
    if ok_flag[k] == 2:
        w2.writelines(f"0000000000{k}"[-10:] + "###" + zh_line[:-1] + " ||| " + en_line)
    elif ok_flag[k] == 1:
        w1.writelines(f"0000000000{k}"[-10:] + "###" + zh_line[:-1] + " ||| " + en_line)
    else:
        w0.writelines(f"0000000000{k}"[-10:] + "###" + zh_line[:-1] + " ||| " + en_line)

f.close()
g.close()
w0.close()
w1.close()
w2.close()
