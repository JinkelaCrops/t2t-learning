# -*- coding: utf-8 -*-
from analyzerutils import Token
from analyzerutils import SentTokenInfo
import json
import argparse

parser = argparse.ArgumentParser(description="analyzerencode.py")
parser.add_argument('-f', "--file_path")
parser.add_argument('--report', default=10000, type=int)

args = parser.parse_args()


if __name__ == '__main__':
    file_path = args.file_path
    file_name = file_path.replace("\\", "/").split("/")[-1]

    tokens = Token()
    lines = []
    file_dict = []
    with open(file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            lines.append(lk.sub_token)
            file_dict.append(lk.sub_order_dict)
            if k % args.report == args.report - 1:
                print(f"analyzerencoder info: execute {file_name} sentence No.{k+1}")

    with open(file_path + ".decode", "w", encoding="utf8") as w0:
        w0.writelines([x+"\n" for x in lines])
    with open(file_path + ".decode.dict", "w", encoding="utf8") as w0_od:
        json.dump(file_dict, w0_od, ensure_ascii=False)
    print(f"analyzerencoder info: write down {file_name}.decode, {file_name}.decode.dict")