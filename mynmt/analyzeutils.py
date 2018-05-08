import re
from regexutils import pattern_sub_pts
from regexutils import pattern_find_pts
from regexutils import mask_update


class RePattern(object):
    @staticmethod
    def regex_between_enzh(regex):
        return f"\\b{regex}(?=[\\u4e00-\\u9fff]|\\b)|(?<=[\\u4e00-\\u9fff]){regex}(?=[\\u4e00-\\u9fff]|\\b)"


class TokenRegexProcess(object):
    level = 1
    regex = " "
    rep = "\\uf000"

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
    rep = "\\uf000"

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
    def __init__(self, verbose=True):
        self.verbose = verbose
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
                if self.verbose:
                    print(f"Token.get_level_map info: {token_name} has level {token_level}")
        return self.level_map

    def set_token_level(self, level_map_part):
        for token_name, token_level in level_map_part.items():
            self.level_map[token_name] = token_level
            if self.verbose:
                print(f"Token.get_level_map info: reset {token_name} 's level to {token_level}")

    class PercentDecimal(TokenRegexProcess):
        level = 1
        """55.55%，必须是小数，允许空格"""
        regex = "[0-9][0-9 ]*\.[0-9 ]*[0-9] *%"
        rep = "PercentDecimal"

    class PercentInteger(TokenRegexProcess):
        level = 0.9
        """100%，必须是整数，允许空格"""
        regex = "[0-9][0-9 ]* *%"
        rep = "PercentInteger"

    class NumericDecimal(TokenRegexProcess):
        level = 1
        """55.55"""
        regex = "[0-9][0-9 ]*\.[0-9 ]*[0-9]"
        rep = "NumericDecimal"

    class NumericInteger(TokenRegexProcess):
        level = 0
        """5"""
        regex = "[0-9][0-9 ]*[0-9]|[0-9]"
        rep = "NumericInteger"

    class NumericYear(TokenRegexProcess):
        level = 0.9
        """2009"""
        regex = RePattern.regex_between_enzh("1[5-9][0-9]{2}") + '|' + RePattern.regex_between_enzh("20[0-9]{2}")
        rep = "NumericYear"

    class TermUpperCase(TokenRegexProcess):
        level = 0.2
        """DNA"""
        regex = RePattern.regex_between_enzh("[A-Z]+")
        rep = "TermUpperCase"

    class TermCamelCase(TokenRegexProcess):
        level = 0.1
        """pH，PubMed, LoL, but not DNA, ID"""
        regex = RePattern.regex_between_enzh("[A-Za-z]+[A-Z]+[A-Za-z]*")
        rep = "TermCamelCase"

    class TermEnCharWithNum(TokenRegexProcess):
        level = 0.3
        """EP2"""
        regex = RePattern.regex_between_enzh("[0-9]*(?:[a-z]*[A-Z]+[a-z]*[0-9]+)+[A-Za-z]*") + "|" + \
                RePattern.regex_between_enzh("[A-Za-z]*(?:[0-9]+[a-z]*[A-Z]+[a-z]*)+[0-9]*")
        rep = "TermEnCharWithNum"

    class TermChemicalPrefix(TokenRegexProcess):
        level = 0.3
        """1,3,7-"""
        regex = "(?<![\w\-])([0-9]+ *[,，] *)*[0-9]+\-(?=[A-Za-z\\u4e00-\\u9fff])"
        rep = "TermChemicalPrefix"

    class RomanNum(TokenSubProcess):
        level = 1
        """Ⅱ"""
        sub_dict = {" ": " "}
        rep = "RomanNum"


class SentTokenInfo(object):
    def __init__(self, sent):
        self.sent = sent
        # self.token_dict = {}
        self.level_dict = {}
        self.pos_dict = {}
        self.filter_piece = []
        self.filter_pos_dict = {}
        self.result = ""
        self.sub_order_dict = []

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
            # self.token_dict[tk.rep] = []

        if filter:
            self.filter_piece = self.max_length_subpiece(self.level_dict)
        else:
            self.filter_piece = self.level_dict.keys()
        for pos in self.filter_piece:
            self.filter_pos_dict[pos] = self.pos_dict[pos]
            # self.token_dict[self.pos_dict[pos]].append(re.sub(" ", "", self.sent[pos[0]:pos[1]]))
        return self.filter_pos_dict  # self.token_dict

    @property
    def sub_token(self):
        if self.result:
            return self.result
        else:
            piece_keys = sorted(self.filter_pos_dict.keys())

            ppp = [0] + [i for p in piece_keys for i in p] + [len(self.sent)]
            ppp = [(ppp[2 * i], ppp[2 * i + 1]) for i in range(len(ppp) // 2)]

            result_ = [self.sent[ppp[0][0]:ppp[0][1]]]
            for k, p in enumerate(piece_keys):
                result_.append(self.filter_pos_dict[piece_keys[k]])
                result_.append(self.sent[ppp[k + 1][0]:ppp[k + 1][1]])
            # TODO: how to get the border of words? here we can use " ".join(result_)
            # any better idea?
            self.result = " ".join(result_)

            self.sub_order_dict = [(self.filter_pos_dict[pos], self.sent[pos[0]:pos[1]].replace(" ", "")) for pos in
                                   piece_keys]
            return self.result


def segment_afterprocess(line):
    line = re.sub(" +", " ", line).strip()
    return line


def sub_sent(sent, sub_order_dict):
    for rep, target in sub_order_dict:
        m = re.search(rep, sent)
        sent = sent[:m.start()] + target + sent[m.end():] if m is not None else sent
    return sent


def decode_sent(sents, sents_dict):
    bad_sents = []
    decode = []
    for k, (sent, sub_dict) in enumerate(zip(sents, sents_dict)):
        try:
            if len(sub_dict) > 0:
                decode.append(sub_sent(sent, sub_dict))
            else:
                decode.append(sent)
        except Exception as e:
            bad_sents.append([sent, sub_dict])
            decode.append(sent)
    if len(bad_sents) > 0:
        print("decode_sent: warning: bad_sent!")
    return decode


def translate_afterprocess(line):
    line = re.sub(" +([,.?!:;'’”})\\]、，。？！：；）】》])", "\\1", line)
    line = re.sub("([,.?!:;'’”})\\]] |[、，。？！：；）】》]) +", "\\1", line)
    line = re.sub("([‘“{(\\[（【《]) +", "\\1", line)
    line = re.sub(" +( [‘“{(\\[]|[（【《])", "\\1", line)

    mask = [0] * len(line)
    # \\b[A-Z]\\. [a-z]+\\b froom corpus
    case_store = ["e. g.", "i. e.", "E. coli", "S. aureus", "O. aureus", "C. indicum", "C. funicola", "M. pusillum"]
    case_regex = "|".join([re.escape(c) for c in case_store])
    case_mask = pattern_find_pts(case_regex, line, mask=mask)
    mask_update(mask, case_mask)

    def upper_after_endmark(m):
        pattern = m.group(0)
        if len(pattern) == 1 and pattern.islower():
            return pattern.upper()
        else:
            return pattern

    line = pattern_sub_pts("(?<=[.?!;] )[a-z]|(?<=[。？！；])[a-z]|(?<=^)[a-z]", upper_after_endmark, line, mask=mask)
    line = re.sub("(?<=[\\u4e00-\\u9fff]) +(?=[\\u4e00-\\u9fff])|"
                  "(?<=[\\u4e00-\\u9fff]) +(?=\\w)|"
                  "(?<=[\\w]) +(?=[\\u4e00-\\u9fff])", "", line)
    line = re.sub(" *([+±=*/<>≤≥_~′″]) *", "\\1", line)
    line = re.sub("(?<!,) *\\- *", "-", line)
    return line


def decode_afterprocess(sents):
    return [translate_afterprocess(sent) for sent in sents]
