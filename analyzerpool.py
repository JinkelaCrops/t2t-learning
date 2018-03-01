import re


class Token(object):
    def __init__(self):
        self.level_map = {}
        self.level_map = self.get_token_level

    @property
    def get_token_name(self):
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
            return re.search("[0-9][0-9 ]*\.[0-9 ]*[0-9] *%", sent) is not None

    class PercentInteger(object):
        level = 0.9

        @staticmethod
        def process(sent):
            """100%，必须是整数，允许空格"""
            return re.search("[0-9][0-9 ]* *%", sent) is not None

    class NumericDecimal(object):
        level = 1

        @staticmethod
        def process(sent):
            """55.55"""
            return re.search("[0-9][0-9 ]*\.[0-9 ]*[0-9]", sent) is not None

    class NumericInteger(object):
        level = 0

        @staticmethod
        def process(sent):
            """5"""
            return re.search("[0-9][0-9 ]*[0-9]", sent) is not None

    class NumericYear(object):
        level = 0.9

        @staticmethod
        def process(sent):
            """2009"""
            return re.search("1[5-9][0-9]{2}|20[0-1][0-9]", sent) is not None

    class TermUpperCase(object):
        level = 0.2

        @staticmethod
        def process(sent):
            """DNA"""
            return re.search("\\b[A-Z]+\\b", sent) is not None

    class TermCamelCase(object):
        level = 0.1

        @staticmethod
        def process(sent):
            """pH，PubMed, LoL, but not DNA, ID"""
            # "\\b[A-Za-z]+[A-Z]+[a-z][A-Za-z]*\\b" # 词中大写
            # "\\b[A-Za-z]+[a-z][A-Z]+\\b"          # 词末大写
            return re.search("\\b[A-Za-z]+[A-Z]+[A-Za-z]*\\b", sent) is not None

    class TermEnCharWithNum(object):
        level = 0.3

        @staticmethod
        def process(sent):
            """EP2"""
            return re.search("\\b[0-9]+[A-Za-z]+[0-9A-Za-z]*\\b|\\b[0-9A-Za-z]+[A-Za-z]+[0-9]+\\b", sent) is not None

    class TermChemicalPrefix(object):
        level = 0.3

        @staticmethod
        def process(sent):
            """1,3,7-"""
            return re.search("(?<![\w\-])([0-9]+ *[,，] *)*[0-9]+\-(?=[A-Za-z\u4000-\u9fff])", sent) is not None


def execute_token(sent, tokens):
    return {token_name: getattr(tokens, token_name).process(sent) for token_name in tokens.get_token_name}

file_path = ""
tokens = Token()
with open(file_path, "r", encoding="utf8") as f:
    f.readlines()
