import re


class Percent(object):
    def __init__(self):
        pass

    class PercentDecimal(object):
        def __init__(self):
            self.level = 1

        @staticmethod
        def process(sent):
            """55.55%，必须是小数，允许空格"""
            return re.search("[0-9][0-9 ]*\.[0-9 ]*[0-9] *%", sent) is not None

    class PercentInteger(object):
        def __init__(self):
            self.level = 0.9

        @staticmethod
        def process(sent):
            """100%，必须是整数，允许空格"""
            return re.search("[0-9][0-9 ]* *%", sent) is not None


class Numeric(object):
    def __init__(self):
        pass

    class NumericDecimal(object):
        def __init__(self):
            self.level = 1

        @staticmethod
        def process(sent):
            """55.55"""
            return re.search("[0-9][0-9 ]*\.[0-9 ]*[0-9]", sent) is not None

    class NumericInteger(object)
        def __init__(self):
            self.level = 0

        @staticmethod
        def process(sent):
            """5"""
            return re.search("[0-9][0-9 ]*[0-9]", sent) is not None

    class NumericYear(object):
        def __init__(self):
            self.level = 0.9

        @staticmethod
        def process(sent):
            """2009"""
            return re.search("1[5-9][0-9]{2}|20[0-1][0-9]", sent) is not None


class Term(object):
    def __init__(self):
        pass

    class UpperCase(object):
        def __init__(self):
            self.level = 0.2

        @staticmethod
        def process(sent):
            """DNA"""
            return re.search("\\b[A-Z]+\\b", sent) is not None

    class CamelCase(object):
        def __init__(self):
            self.level = 0.1

        @staticmethod
        def process(sent):
            """pH，PubMed, LoL, but not DNA, ID"""
            # "\\b[A-Za-z]+[A-Z]+[a-z][A-Za-z]*\\b" # 词中大写
            # "\\b[A-Za-z]+[a-z][A-Z]+\\b"          # 词末大写
            return re.search("\\b[A-Za-z]+[A-Z]+[A-Za-z]*\\b", sent) is not None

    class EnCharWithNum(object):
        def __init__(self):
            self.level = 0.3

        @staticmethod
        def process(sent):
            """EP2"""
            return re.search("\\b[0-9]+[A-Za-z]+[0-9A-Za-z]*\\b|\\b[0-9A-Za-z]+[A-Za-z]+[0-9]+\\b", sent) is not None

    class ChemicalPrefix(object):
        def __init__(self):
            self.level = 0.3

        @staticmethod
        def process(sent):
            """1,3,7-"""
            return re.search("(?<![\w\-])([0-9]+ *[,，] *)*[0-9]+\-(?=[A-Za-z\u4000-\u9fff])", sent) is not None

    class Chemical(object):
        def __init__(self):
            self.level = 1
