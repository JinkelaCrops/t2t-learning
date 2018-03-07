# -*- coding: utf-8 -*-
from analyzerutils import Token
from analyzerutils import SentTokenInfo
import json
import re
import argparse

parser = argparse.ArgumentParser(description="analyzerencoder.py")
parser.add_argument('-f', "--file_path_prefix")
parser.add_argument('--report', default=10000, type=int)

args = parser.parse_args()


if __name__ == '__main__':
    file_path_prefix = args.file_path_prefix
    zh_file_path = file_path_prefix + ".zh"
    en_file_path = file_path_prefix + ".en"

    tokens = Token()
    zh_lines = []
    zh_file_dict = []
    with open(zh_file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            zh_lines.append(lk.sub_token)
            zh_file_dict.append(lk.sub_order_dict)
            if k % args.report == args.report - 1:
                print(f"analyzerencoder info: execute zh sentence No.{k+1}")

    en_lines = []
    en_file_dict = []
    with open(en_file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            en_lines.append(lk.sub_token)
            en_file_dict.append(lk.sub_order_dict)
            if k % args.report == args.report - 1:
                print(f"analyzerencoder info: execute en sentence No.{k+1}")

    with open(file_path_prefix + ".decode.zh", "w", encoding="utf8") as w0:
        w0.writelines([x+"\n" for x in zh_lines])
    with open(file_path_prefix + ".decode.en", "w", encoding="utf8") as w0:
        w0.writelines([x+"\n" for x in en_lines])
    with open(file_path_prefix + ".decode.zh.dict", "w", encoding="utf8") as w0_od:
        json.dump(zh_file_dict, w0_od, ensure_ascii=False)
    with open(file_path_prefix + ".decode.en.dict", "w", encoding="utf8") as w0_od:
        json.dump(en_file_dict, w0_od, ensure_ascii=False)
    assert 1 > 2