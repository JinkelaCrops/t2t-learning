import re
import numpy as np


# from collections import OrderedDict


# import argparse
#
# parser = argparse.ArgumentParser(description="analyzerpool.py")
# parser.add_argument('-f', "--file_path_prefix")
#
# args = parser.parse_args()

class TokenProcess(object):
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

    class PercentDecimal(TokenProcess):
        level = 1
        """55.55%，必须是小数，允许空格"""
        regex = "[0-9][0-9 ]*\.[0-9 ]*[0-9] *%"
        rep = "\uf000"

    class PercentInteger(TokenProcess):
        level = 0.9
        """100%，必须是整数，允许空格"""
        regex = "[0-9][0-9 ]* *%"
        rep = "\uf001"

    class NumericDecimal(TokenProcess):
        level = 1
        """55.55"""
        regex = "[0-9][0-9 ]*\.[0-9 ]*[0-9]"
        rep = "\uf002"

    class NumericInteger(TokenProcess):
        level = 0
        """5"""
        regex = "[0-9][0-9 ]*[0-9]|[0-9]"
        rep = "\uf003"

    class NumericYear(TokenProcess):
        level = 0.9
        """2009"""
        regex = "1[5-9][0-9]{2}|20[0-1][0-9]"
        rep = "\uf004"

    class TermUpperCase(TokenProcess):
        level = 0.2
        """DNA"""
        regex = "\\b[A-Z]+\\b"
        rep = "\uf005"

    class TermCamelCase(TokenProcess):
        level = 0.1
        """pH，PubMed, LoL, but not DNA, ID"""
        regex = "\\b[A-Za-z]+[A-Z]+[A-Za-z]*\\b"
        rep = "\uf006"

    class TermEnCharWithNum(TokenProcess):
        level = 0.3
        """EP2"""
        regex = "\\b[0-9]+[A-Za-z]+[0-9A-Za-z]*\\b|\\b[0-9A-Za-z]*[A-Za-z]+[0-9]+\\b"
        rep = "\uf007"

    class TermChemicalPrefix(TokenProcess):
        level = 0.3
        """1,3,7-"""
        regex = "(?<![\w\-])([0-9]+ *[,，] *)*[0-9]+\-(?=[A-Za-z\u4000-\u9fff])"
        rep = "\uf008"


class SentTokenInfo(object):
    def __init__(self, sent):
        self.sent = sent
        self.token_dict = {}
        self.level_dict = {}
        self.pos_dict = {}
        self.filter_piece = []
        self.filter_pos_dict = {}
        self.result = sent

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

    def sub_token(self):
        for pos, rep in self.filter_pos_dict.items():
            self.result = self.result[:pos[0]] + rep * (pos[1] - pos[0]) + self.result[pos[1]:]
        self.result = re.sub("([\uf000-\uf009])+", "\\1", self.result)
        return self.result


# if __name__ == '__main__':
#     zh = "结果在分离的3 947株病原菌中,革兰阴性菌3 169株(80. 3%),革兰阳性菌778株(19. 7%)。"
#     tokens = Token()
#     lk = SentTokenInfo(zh)
#     lk.execute_token(tokens)
#     print(lk.filter_piece)

if __name__ == "__main__":
    file_path_prefix = "../t2t_med/t2t_datagen/medicine/medicine.sample.big.txt"
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

    nonempty_line = []
    empty_line = []
    w0 = open(file_path_prefix + ".term_error.ed1", "w", encoding="utf8")
    w1 = open(file_path_prefix + ".term_empty.ed1", "w", encoding="utf8")
    w2 = open(file_path_prefix + ".term_nonempty.ed1", "w", encoding="utf8")

    for k in range(len(zh_file_dict)):
        if ok_flag[k] == 2:
            w2.writelines(
                f"0000000000{k}"[-10:] + "###" + zh_file_dict[k].sub_token() + " ||| " + en_file_dict[k].sub_token() + "\n")
        elif ok_flag[k] == 1:
            w1.writelines(
                f"0000000000{k}"[-10:] + "###" + zh_file_dict[k].sub_token() + " ||| " + en_file_dict[k].sub_token() + "\n")
        else:
            w0.writelines(
                f"0000000000{k}"[-10:] + "###" + zh_file_dict[k].sub_token() + " ||| " + en_file_dict[k].sub_token() + "\n")

    w0.close()
    w1.close()
    w2.close()

