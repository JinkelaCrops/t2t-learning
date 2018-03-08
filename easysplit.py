# -*- coding: utf-8 -*-
import random
import json
import sys
import argparse

parser = argparse.ArgumentParser(description="easysplit.py")
parser.add_argument('-f', "--file_path")
parser.add_argument('--train', default="train")
parser.add_argument('--valid', default="valid")
parser.add_argument("--valid_size", default=10000, type=int)
parser.add_argument("--shuffle", default=True, type=bool)
args = parser.parse_args()


def train_valid_split(file_path, file_dir, train_name, valid_name, size=10000, shuffle=True):
    with open(file_path, "r", encoding="utf8") as f:
        data = f.readlines()

    if shuffle:
        random.seed(0)
        data = random.sample(data, len(data))

    with open(f"{file_dir}/{train_name}", "w", encoding="utf8") as f:
        f.writelines(data[:-size])
    with open(f"{file_dir}/{valid_name}", "w", encoding="utf8") as f:
        f.writelines(data[-size:])
    return 0


if __name__ == '__main__':
    file_path = args.file_path
    file_name = file_path.replace("\\", "/").split("/")[-1]
    file_dir = "/".join(file_path.replace("\\", "/").split("/")[:-1])

    train_valid_split(file_path, file_dir, args.train, args.valid, args.valid_size, args.shuffle)
