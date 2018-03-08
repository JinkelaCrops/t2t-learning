# -*- coding: utf-8 -*-
import re
import argparse

parser = argparse.ArgumentParser(description="filter.py")
parser.add_argument('-f', "--file_path")
parser.add_argument('-s', "--separator", default="\t")

args = parser.parse_args()


class Filter(object):
    def __init__(self, sep):
        self.sep = sep

    @staticmethod
    def with_reg(reg, string_lst):
        return list(filter(lambda string: re.search(reg, string) is not None, string_lst))

    @staticmethod
    def without_reg(reg, string_lst):
        return list(filter(lambda string: re.search(reg, string) is None, string_lst))

    def replace_bad_sep(self, bi_lines, new_sep):
        bi_lines = [bi_line.replace(self.sep, new_sep) for bi_line in bi_lines]
        self.sep = new_sep
        return bi_lines

    def tridots_filter(self, bi_lines):
        """
        filter tridots such as ...
        """
        bi_lines = self.without_reg("\.{2,}", bi_lines)
        return bi_lines

    def simple_filter(self, bi_lines):
        """
        simple, only have A-Za-z \u4000-\u9fff ,. ，。in sentence
        """
        bi_lines = self.without_reg("[^A-Za-z\u4000-\u9fff %s\n\.,。，]" % self.sep, bi_lines)
        return bi_lines

    def general_filter(self, bi_lines):
        """
        general, have 0-9 A-Za-z \u4000-\u9fff ,. ，。?？!！in sentence
        """
        bi_lines = self.without_reg("[^0-9A-Za-z\u4000-\u9fff,\.，。\?？\!！]", bi_lines)
        return bi_lines

    def clear_filter(self, bi_lines):
        """
        clear, have \u4000-\u9fff in only one side
        """
        bi_lines = self.simple_filter(bi_lines)
        bi_lines = self.without_reg("[\u4000-\u9fff][^%s]*%s[^%s]*[\u4000-\u9fff]" % (self.sep, self.sep, self.sep),
                                    bi_lines)
        return bi_lines


if __name__ == '__main__':
    sep = args.separator
    file_path = args.file_path
    file_name = file_path.replace("\\", "/").split("/")[-1]
    file_father_dir = "/".join(file_path.replace("\\", "/").split("/")[:-1])

    with open(file_path, "r", encoding="utf8") as f:
        data = f.readlines()
    # filter
    line_filter = Filter(sep)
    data = line_filter.replace_bad_sep(data, "\u0000")
    data = line_filter.tridots_filter(data)
    data = line_filter.clear_filter(data)
    data = line_filter.replace_bad_sep(data, sep)
    print(f"filter info: num of filter lines: {len(data)}")

    with open(f"{file_path}.filter", "w", encoding="utf8") as f:
        f.writelines(data)
