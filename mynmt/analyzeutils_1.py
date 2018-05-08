import re


def pattern_find_all(regex, sent, group=0):
    output = []
    for x in re.finditer(regex, sent):
        output.append(x.group(group))
    return output


def _flatten_region_to_region(flatten_region, strip=True):
    if strip:
        if len(flatten_region) > 0 and flatten_region[0] == flatten_region[1]:
            flatten_region = flatten_region[2:]
        if len(flatten_region) > 0 and flatten_region[-1] == flatten_region[-2]:
            flatten_region = flatten_region[:-2]
    if len(flatten_region) % 2 > 0:
        flatten_region.pop(-1)
    region = []
    for i in range(len(flatten_region) // 2):
        region.append(flatten_region[2 * i: 2 * i + 2])
    return region


def gen_unmasked_region(mask: list):
    mask_region_tmp = [0]
    continue_flag = False
    for k, current_state in enumerate(mask):
        if continue_flag ^ current_state:
            continue_flag = not continue_flag
            mask_region_tmp.append(k)
    mask_region_tmp.append(len(mask))
    mask_region = _flatten_region_to_region(mask_region_tmp)
    return mask_region


def mask_update(mask, pts: dict):
    if not pts:
        return
    for i, pti in pts.items():
        for j in pti:
            for k in range(j[0], j[1]):
                mask[k] = 1


def pattern_sub_pts(regex, sent, flags=0, group=0, mask=None) -> str:
    return " ".join(output_list)


def pattern_find_pts(regex, sent, flags=0, group=0, mask=None) -> dict:
    if "(?=" in regex or "(?!" in regex:
        raise Exception("do not support look ahead, for finditer will block all str behind endpos")
    mask = [0] * len(sent) if mask is None else mask
    unmasked_region = gen_unmasked_region(mask)
    output = {}
    p = re.compile(regex, flags=flags)
    for region in unmasked_region:
        for x in p.finditer(sent, region[0], region[1]):
            position = [x.start(), x.end()]
            pattern = x.group(group)
            if pattern in output:
                output[pattern].append(position)
            else:
                output[pattern] = [position]
    return output


class Field(object):
    def __init__(self, line):
        self.line = line
        self.mask = [0] * len(self.line)


class Rule(object):
    def __init__(self):
        self.id = 0
        self.desc = "This is a rule"
        self.level = 0
        self.regex = ""

    def process(self, field: Field):
        output = None
        if self.regex:
            output = pattern_find_pts(self.regex, field.line, mask=field.mask)
        mask_update(field.mask, output)
        return output


class Check(object):
    pass


class Modify(object):
    def __init__(self):
        pass

    class Link(Rule):
        def __init__(self):
            super().__init__()
            self.desc = "TTTLink"
            self.regex = "(?:(?:ht|f)tps?://[\\w+\\-]+|www\\.)[\\w\\-\\.,@\\?=%&:;/~\\+#]+/?"
            assert re.fullmatch(self.regex, "http://dswd.com")

    class Email(Rule):
        def __init__(self):
            super().__init__()
            self.desc = "TTTEmail"
            self.regex = "[\\w\\-]+@[\\w\\-]+(?:\\.[\\w\\-]+)+"
            assert re.fullmatch(self.regex, "dasd@dasds.edu")

    class Numeric(Rule):
        def __init__(self):
            super().__init__()
            self.desc = "TTTNumeric"
            self.regex = "\\b[0-9][0-9 ]*(\\.[0-9 ]*[0-9]+)?\\b"
            assert re.search(self.regex, "ewe 6 0. 9 0%单位")

        def process(self, field: Field):
            output = pattern_find_pts(self.regex, field.line, flags=re.A.value, mask=field.mask)
            mask_update(field.mask, output)
            # sub with self.desc
            region_tmp = [0] + [k for i, pti in output.items() for j in pti for k in j] + [len(field.line)]
            region = _flatten_region_to_region(region_tmp, strip=False)
            output_list = []
            for k, region_k in enumerate(region):
                if k < len(region) - 1:
                    output_list.append(field.line[region_k[0]:region_k[1]])
                    output_list.append(self.desc)
            output_list.append(field.line[region[-1][0]:region[-1][1]])
            field.line = " ".join(output_list)
            return output

    class UpperChemical(Numeric):
        def __init__(self):
            super().__init__()
            self.desc = "TTTUpperChemical"
            self.regex = "\\b[A-Z][A-Z0-9_]+\\b"
            assert re.search(self.regex, "ewe 6 0. 9 0%单位")

    class ComplicateChemical(Numeric):
        def __init__(self):
            super().__init__()
            self.desc = "TTTComplicateChemical"
            # TODO:
            self.regex = "\\b[A-Z][A-Z0-9_]+\\b"
            assert re.fullmatch(self.regex, "4(3H)-oxo-5,6,7,8-tetrahydropyrido-[2,3-d]")


field = Field("http://www.baidu.666.com H1E2 6 0. 9 0%单位988")
Modify.Link().process(field)
Modify.Email().process(field)
Modify.Numeric().process(field)


class Filter:
    pass


class RePattern(object):
    @staticmethod
    def regex_between_enzh(regex):
        return f"\\b{regex}(?=[\u4e00-\u9fff]|\\b)|(?<=[\u4e00-\u9fff]){regex}(?=[\u4e00-\u9fff]|\\b)"


class TokenRegexProcess(object):
    regex = " "

    @classmethod
    def process(cls, sent):
        # TODO: SubwordTextEncoder, and the paper with group sub
        matcher = re.finditer(cls.regex, sent)
        pattern = [0]
        for k, m in enumerate(matcher):
            pattern.append((m.start(), m.end()))
        pattern.append(len(sent))
        if len(pattern) >= 2 and pattern[0] == pattern[1]:
            pattern.pop(0)
            pattern.pop(0)
        if len(pattern) >= 2 and pattern[-1] == pattern[-2]:
            pattern.pop(-1)
            pattern.pop(-1)
        return pattern


class TokenSubProcess(object):
    level = 1
    sub_dict = {" ": " "}
    rep = "\u0000"

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

    class Link(TokenRegexProcess):
        regex = "(?:(?:ht|f)tps?://[\w+\-]+|www\.)[\w\-\.,@\?=%&:;/~\+#]+/?"
        assert re.search("^" + regex + "$", "http://dswd.com") is not None

    class Email(TokenRegexProcess):
        regex = "[\w\-]+@[\w\-]+(?:\.[\w\-]+)+"
        assert re.search("^" + regex + "$", "dasd@dasds.edu") is not None

    class PercentNumeric(TokenRegexProcess):
        regex = "(?<=[\u4000-\u9fff ])[0-9][0-9 ]*(\.[0-9 ]*[0-9]+)? *[%‰‱]?(?=[\u4000-\u9fff ])"
        assert re.search(regex, "ewe 6 0. 9 0%单位")

    class Numeric(TokenRegexProcess):
        regex = "(?<=[\u4000-\u9fff ])[0-9][0-9 ]*(\.[0-9 ]*[0-9]+)?(?=[\u4000-\u9fff ])"
        assert re.search(regex, "ewe 6 0. 9 0单位")

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
        regex = RePattern.regex_between_enzh("[0-9]+[A-Za-z]+[0-9A-Za-z]*") + "|" + RePattern.regex_between_enzh(
            "[0-9A-Za-z]*[A-Za-z]+[0-9]+")
        rep = "TermEnCharWithNum"

    class TermChemicalPrefix(TokenRegexProcess):
        level = 0.3
        """1,3,7-"""
        regex = "(?<![\w\-])([0-9]+ *[,，] *)*[0-9]+\-(?=[A-Za-z\u4e00-\u9fff])"
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

            self.sub_order_dict = [(self.filter_pos_dict[pos], self.sent[pos[0]:pos[1]]) for pos in piece_keys]
            return self.result


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
