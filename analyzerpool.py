# -*- coding: utf-8 -*-
import re
import numpy as np
import json
import argparse

parser = argparse.ArgumentParser(description="analyzerpool.py")
parser.add_argument('-f', "--file_path_prefix")

args = parser.parse_args()

# from collections import OrderedDict


# import argparse
#
# parser = argparse.ArgumentParser(description="analyzerpool.py")
# parser.add_argument('-f', "--file_path_prefix")
#
# args = parser.parse_args()

class RePattern(object):
    @staticmethod
    def regex_between_enzh(regex):
        return f"\\b{regex}(?=[\u4000-\u9fff]|\\b)|(?<=[\u4000-\u9fff]){regex}(?=[\u4000-\u9fff]|\\b)"


class TokenRegexProcess(object):
    level = 1
    regex = " "
    rep = "\uf000"

    @classmethod
    def process(cls, sent):
        # TODO: SubwordTextEncoder, and the paper with group sub
        matcher = re.finditer(cls.regex, sent)
        pattern = []
        for k, m in enumerate(matcher):
            pattern.append((m.start(), m.end()))
        return pattern


class TokenSubProcess(object):
    level = 1
    sub_dict = {" ": " "}
    rep = "\uf000"

    @classmethod
    def process(cls, sent):
        pattern = []
        for src_wd, tgt_wd in cls.sub_dict.items():
            matcher = re.finditer(re.escape(src_wd), sent)
            pattern = []
            for k, m in enumerate(matcher):
                pattern.append((m.start(), m.end()))
        return pattern


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

    class PercentDecimal(TokenRegexProcess):
        level = 1
        """55.55%，必须是小数，允许空格"""
        regex = "[0-9][0-9 ]*\.[0-9 ]*[0-9] *%"
        rep = "\uf000"

    class PercentInteger(TokenRegexProcess):
        level = 0.9
        """100%，必须是整数，允许空格"""
        regex = "[0-9][0-9 ]* *%"
        rep = "\uf001"

    class NumericDecimal(TokenRegexProcess):
        level = 1
        """55.55"""
        regex = "[0-9][0-9 ]*\.[0-9 ]*[0-9]"
        rep = "\uf002"

    class NumericInteger(TokenRegexProcess):
        level = 0
        """5"""
        regex = "[0-9][0-9 ]*[0-9]|[0-9]"
        rep = "\uf003"

    class NumericYear(TokenRegexProcess):
        level = 0.9
        """2009"""
        regex = RePattern.regex_between_enzh("1[5-9][0-9]{2}") + '|' + RePattern.regex_between_enzh("20[0-9]{2}")
        rep = "\uf004"

    class TermUpperCase(TokenRegexProcess):
        level = 0.2
        """DNA"""
        regex = RePattern.regex_between_enzh("[A-Z]+")
        rep = "\uf005"

    class TermCamelCase(TokenRegexProcess):
        level = 0.1
        """pH，PubMed, LoL, but not DNA, ID"""
        regex = RePattern.regex_between_enzh("[A-Za-z]+[A-Z]+[A-Za-z]*")
        rep = "\uf006"

    class TermEnCharWithNum(TokenRegexProcess):
        level = 0.3
        """EP2"""
        regex = RePattern.regex_between_enzh("[0-9]+[A-Za-z]+[0-9A-Za-z]*") + "|" + RePattern.regex_between_enzh(
            "[0-9A-Za-z]*[A-Za-z]+[0-9]+")
        rep = "\uf007"

    class TermChemicalPrefix(TokenRegexProcess):
        level = 0.3
        """1,3,7-"""
        regex = "(?<![\w\-])([0-9]+ *[,，] *)*[0-9]+\-(?=[A-Za-z\u4000-\u9fff])"
        rep = "\uf008"

    class RomanNum(TokenSubProcess):
        level = 1
        """Ⅱ"""
        sub_dict = {" ": " "}
        rep = "\uf009"


class SentTokenInfo(object):
    def __init__(self, sent):
        self.sent = sent
        self.token_dict = {}
        self.level_dict = {}
        self.pos_dict = {}
        self.filter_piece = []
        self.filter_pos_dict = {}
        self.result = ""
        self.sub_order_dict = {}

    @staticmethod
    def sub_space(targets):
        return [re.sub(" ", "", target) for target in targets]

    @staticmethod
    def max_length_subpiece(piece_level_dict):
        """
        pos:[(1,2), (3,4), (1,4)] and level:[2, 2, 1] -> [(1,4)]
        pos:[(2,4), (3,5), (5,8)] and level:[1, 2, 1] -> [(3,5), (5,8)]
        """
        piece_keys = sorted(piece_level_dict.keys())
        if len(piece_keys) == 0:
            return []
        filter_piece_tmp = []
        __ = 0
        his_ = 0
        for _, i in enumerate(piece_keys):
            if (_ <= his_ + __) and (_ > 0):
                continue
            __ = 0
            li = piece_level_dict[i]
            tmp = (i, li)
            for j in piece_keys:
                lj = piece_level_dict[j]
                if tmp[0] == j:
                    pass
                elif ((tmp[0][0] < j[0]) and (tmp[0][1] >= j[1])) or ((tmp[0][0] <= j[0]) and (tmp[0][1] > j[1])):
                    tmp = tmp
                    __ += 1
                elif ((tmp[0][0] >= j[0]) and (tmp[0][1] < j[1])) or ((tmp[0][0] > j[0]) and (tmp[0][1] <= j[1])):
                    tmp = (j, lj)
                    __ += 1
                elif ((tmp[0][0] > j[0]) and (tmp[0][1] > j[1]) and (tmp[0][0] < j[1])) or (
                        (tmp[0][0] < j[0]) and (tmp[0][1] < j[1]) and (tmp[0][1] > j[0])):
                    tmp = tmp if tmp[1] >= lj else (j, lj)
                    __ += 1
                else:
                    pass
            filter_piece_tmp.append(tmp)
            his_ = _
        filter_piece_tmp = sorted(list(set(filter_piece_tmp)))
        filter_piece_tmp = list(zip(*filter_piece_tmp))
        return filter_piece_tmp[0]

    def execute_token(self, tokens, filter=True):
        for token_name in tokens.get_token_name:
            tk = getattr(tokens, token_name)
            pattern = tk.process(self.sent)
            for pos in pattern:
                if pos not in self.level_dict or self.level_dict[pos] < tk.level:
                    self.level_dict[pos] = tk.level
                    self.pos_dict[pos] = tk.rep
            self.token_dict[tk.rep] = []

        if filter:
            self.filter_piece = self.max_length_subpiece(self.level_dict)
        else:
            self.filter_piece = self.level_dict.keys()
        for pos in self.filter_piece:
            self.filter_pos_dict[pos] = self.pos_dict[pos]
            self.token_dict[self.pos_dict[pos]].append(re.sub(" ", "", self.sent[pos[0]:pos[1]]))
        return self.token_dict, self.filter_pos_dict

    @property
    def sub_token(self):
        if self.result:
            return self.result
        else:
            self.result = self.sent
            piece_keys = sorted(self.filter_pos_dict.keys())
            for pos in piece_keys:
                rep = self.filter_pos_dict[pos]
                self.result = self.result[:pos[0]] + rep * (pos[1] - pos[0]) + self.result[pos[1]:]
            self.result = re.sub("([\uf000-\uf009])+", "\\1", self.result)

            self.sub_order_dict = [(self.filter_pos_dict[pos], re.sub(" ", "", self.sent[pos[0]:pos[1]])) for pos in
                                   piece_keys]
            return self.result


def sub_sent(sent, sub_order_dict):
    for rep, target in sub_order_dict:
        m = re.search(rep, sent)
        sent = sent[:m.start()] + target + sent[m.end():]
    return sent


# if __name__ == '__main__':
#     zh = "结果在分离的3 947株病原菌中,革兰阴性菌3 169株(80. 3%),革兰阳性菌778株(19. 7%)。"
#     tokens = Token()
#     lk = SentTokenInfo(zh)
#     lk.execute_token(tokens)
#     print(lk.filter_piece)

if __name__ == "__main__":
    file_path_prefix = args.file_path_prefix
    zh_file_path = file_path_prefix + ".zh"
    en_file_path = file_path_prefix + ".en"

    tokens = Token()
    zh_file_dict = {}
    with open(zh_file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            zh_file_dict[k] = lk

    en_file_dict = {}
    with open(en_file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            en_file_dict[k] = lk


    def flag_gen(i):
        if zh_file_dict[i].token_dict == en_file_dict[i].token_dict:
            if any(zh_file_dict[i].token_dict.values()):
                return 2
            else:
                return 1
        else:
            return 0


    ok_flag = [flag_gen(i) for i in range(len(zh_file_dict))]
    print(np.mean(np.array(ok_flag) > 0))
    print(np.mean(np.array(ok_flag) == 1))
    print(np.mean(np.array(ok_flag) == 2))

    w0_lines = []
    w0_order_dict = []
    w1_lines = []
    w1_order_dict = []
    w2_lines = []
    w2_order_dict = []

    line_k = lambda k: f"00000000{k}"[-10:] + "###" \
                       + zh_file_dict[k].sub_token + " ||| " \
                       + en_file_dict[k].sub_token + "\n"

    for k in range(len(zh_file_dict)):
        if ok_flag[k] == 2:
            w2_lines.append(line_k(k))
            w2_order_dict.append(zh_file_dict[k].sub_order_dict)
        elif ok_flag[k] == 1:
            w1_lines.append(line_k(k))
            w1_order_dict.append(zh_file_dict[k].sub_order_dict)
        else:
            w0_lines.append(line_k(k))
            w0_order_dict.append(zh_file_dict[k].sub_order_dict)

    # use train.dict for the order is mostly the same
    filter_func = lambda k: zh_file_dict[k].sub_order_dict != en_file_dict[k].sub_order_dict and \
                            any([zh_file_dict[k].token_dict[p] != en_file_dict[k].token_dict[p] for p in
                                 zh_file_dict[k].token_dict.keys()])
    order_flag = [filter_func(k) for k in range(len(zh_file_dict)) if ok_flag[k] > 0]
    print("different order percent: %5f" % (sum(order_flag) / len(order_flag)))

    with open(file_path_prefix + ".term_error", "w", encoding="utf8") as w0:
        w0.writelines(w0_lines)
    with open(file_path_prefix + ".term_error.dict", "w", encoding="utf8") as w0_od:
        json.dump(w0_order_dict, w0_od, ensure_ascii=False)

    with open(file_path_prefix + ".term_empty", "w", encoding="utf8") as w1:
        w1.writelines(w1_lines)
    with open(file_path_prefix + ".term_empty.dict", "w", encoding="utf8") as w1_od:
        json.dump(w1_order_dict, w1_od, ensure_ascii=False)

    with open(file_path_prefix + ".term_nonempty", "w", encoding="utf8") as w2:
        w2.writelines(w2_lines)
    with open(file_path_prefix + ".term_nonempty.dict", "w", encoding="utf8") as w2_od:
        json.dump(w2_order_dict, w2_od, ensure_ascii=False)
