# -*- coding: utf-8 -*-
from textfilterutils import Unpack
import argparse

parser = argparse.ArgumentParser(description="unpack.py")

parser.add_argument('-f', "--file_path")
parser.add_argument('-s', "--separator", default="\t")

args = parser.parse_args()

if __name__ == "__main__":
    sep = args.separator
    file_path = args.file_path
    file_name = file_path.replace("\\", "/").split("/")[-1]

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
                print(f"unpack error: {e.__class__}, {e.__context__}, ### {line.strip()}")
                pass

    print(f"unpack info: export to {file_name}.zh and {file_name}.en")
    with open(file_path + ".zh", "w", encoding="utf8") as f:
        f.writelines(["%s\n" % zh for zh in zh_lines])
    with open(file_path + ".en", "w", encoding="utf8") as f:
        f.writelines(["%s\n" % en for en in en_lines])
