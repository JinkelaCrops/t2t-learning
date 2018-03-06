# -*- coding: utf-8 -*-
import random
import argparse

parser = argparse.ArgumentParser(description="trainvalidsplit.py")
parser.add_argument('-f', "--file_path_prefix")
parser.add_argument('-z', "--valid_size", default=10000, type=int)
parser.add_argument('-s', "--shuffle", default=True, type=bool)

args = parser.parse_args()

if __name__ == '__main__':
    file_path_prefix = args.file_path_prefix
    file_prefix = file_path_prefix.replace("\\", "/").split("/")[-1]
    file_father_dir = "/".join(file_path_prefix.replace("\\", "/").split("/")[:-1])

    zh_file_path = file_path_prefix + ".zh"
    en_file_path = file_path_prefix + ".en"

    valid_size = args.valid_size
    # input zh
    with open(zh_file_path, "r", encoding="utf8") as f:
        zh_data = f.readlines()

    # shuffle zh
    if args.shuffle:
        random.seed(0)
        zh_data = random.sample(zh_data, len(zh_data))

    # zh train valid output
    with open(f"{file_father_dir}/train.zh", "w", encoding="utf8") as f:
        f.writelines(zh_data[:-valid_size])
    with open(f"{file_father_dir}/valid.zh", "w", encoding="utf8") as f:
        f.writelines(zh_data[-valid_size:])
    del zh_data

    # input en
    with open(en_file_path, "r", encoding="utf8") as f:
        en_data = f.readlines()

    # shuffle en
    if args.shuffle:
        random.seed(0)
        en_data = random.sample(en_data, len(en_data))

    # en train valid output
    with open(f"{file_father_dir}/train.en", "w", encoding="utf8") as f:
        f.writelines(en_data[:-valid_size])
    with open(f"{file_father_dir}/valid.en", "w", encoding="utf8") as f:
        f.writelines(en_data[-valid_size:])
    del en_data
