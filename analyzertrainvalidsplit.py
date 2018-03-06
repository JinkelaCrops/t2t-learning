# -*- coding: utf-8 -*-
import random
import argparse

parser = argparse.ArgumentParser(description="analyzertrainvalidsplit.py")
parser.add_argument('-f', "--file_path_prefix")
parser.add_argument("--valid_size", default=10000, type=int)
parser.add_argument("--shuffle", default=True, type=bool)

args = parser.parse_args()


def train_valid_split(file_path, file_dir, suffix, size=10000, shuffle=True):
    with open(file_path, "r", encoding="utf8") as f:
        data = f.readlines()

    if shuffle:
        random.seed(0)
        data = random.sample(data, len(data))

    with open(f"{file_dir}/train.{suffix}", "w", encoding="utf8") as f:
        f.writelines(data[:-size])
    with open(f"{file_dir}/valid.{suffix}", "w", encoding="utf8") as f:
        f.writelines(data[-size:])
    del data
    return 0


if __name__ == '__main__':
    file_path_prefix = args.file_path_prefix
    file_prefix = file_path_prefix.replace("\\", "/").split("/")[-1]
    file_father_dir = "/".join(file_path_prefix.replace("\\", "/").split("/")[:-1])

    zh_file_path = file_path_prefix + ".zh"
    en_file_path = file_path_prefix + ".en"
    zh_file_dict_path = file_path_prefix + ".dict"

    train_valid_split(zh_file_path, file_father_dir, "zh", args.valid_size, args.shuffle)
    train_valid_split(en_file_path, file_father_dir, "en", args.valid_size, args.shuffle)
    train_valid_split(zh_file_dict_path, file_father_dir, "dict", args.valid_size, args.shuffle)
