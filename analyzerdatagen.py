# -*- coding: utf-8 -*-
import re
import json
import random
import argparse

parser = argparse.ArgumentParser(description="analyzerdatagen.py")
parser.add_argument('-f', "--file_path_prefix")
parser.add_argument("--separator")

args = parser.parse_args()


def unpack(line, sep=" ||| "):
    zh, en = line.strip().split(sep)
    return zh, en


if __name__ == '__main__':
    file_path_prefix = args.file_path_prefix
    filename_list = [file_path_prefix + ".term_nonempty",
                     file_path_prefix + ".term_empty", ]

    data = []
    data_dict = []
    for filename in filename_list:
        with open(filename, "r", encoding="utf8") as f:
            data += f.readlines()
        with open(filename + ".dict", "r", encoding="utf8") as fd:
            data_dict += json.load(fd)

    zhs = []
    ens = []
    for line in data:
        try:
            zh, en = unpack(line, sep=args.separator)
            zhs.append(zh)
            ens.append(en)
        except Exception as e:
            print(line)

    with open(f"{file_path_prefix}.term.en", "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in ens])
    with open(f"{file_path_prefix}.term.zh", "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in zhs])
    # use train.dict for the order is mostly the same
    with open(f"{file_path_prefix}.term.dict", "w", encoding="utf8") as f:
        json.dump(data_dict, f, ensure_ascii=False)
