# -*- coding: utf-8 -*-
from analyzerutils import Token
from analyzerutils import SentTokenInfo
import numpy as np
import json
import sys
# from concurrent.futures import ProcessPoolExecutor
import argparse

parser = argparse.ArgumentParser(description="analyzerpool.py")
parser.add_argument('-f', "--file_path_prefix")
parser.add_argument('--report', default=10000, type=int)

args = parser.parse_args()


# from collections import OrderedDict


# import argparse
#
# parser = argparse.ArgumentParser(description="analyzerpool.py")
# parser.add_argument('-f', "--file_path_prefix")
#
# args = parser.parse_args()



# def main(data_with_lineNo, tokens):
#     data_file_dict = {}
#     for k, line in data_with_lineNo.items():
#         lk = SentTokenInfo(line[:-1])
#         lk.execute_token(tokens)
#         data_file_dict[k] = lk
#     return data_file_dict

#     myexecutor = ProcessPoolExecutor(max_workers=opt.workers)
#     myexecutor.map()


# if __name__ == '__main__':
#     zh = "Result ais 在分离的 3 947 株病原菌中，革兰阴性菌 3 169 株 (80. 3%), 革兰阳性菌 778 株 (19. 7%)。"
#     tokens = Token()
#     lk = SentTokenInfo(zh)
#     lk.execute_token(tokens)
#     print(lk.filter_piece)


if __name__ == "__main__":
    file_path_prefix = args.file_path_prefix
    zh_file_path = file_path_prefix + ".zh"
    en_file_path = file_path_prefix + ".en"

    tokens = Token()
    zh_file_dict = {}
    with open(zh_file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            zh_file_dict[k] = lk
            if k % args.report == args.report - 1:
                print(f"analyzerpool info: execute zh sentence No.{k+1}")

    en_file_dict = {}
    with open(en_file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            en_file_dict[k] = lk
            if k % args.report == args.report - 1:
                print(f"analyzerpool info: execute en sentence No.{k+1}")


    def flag_gen(i):
        if zh_file_dict[i].token_dict == en_file_dict[i].token_dict:
            if any(zh_file_dict[i].token_dict.values()):
                return 2
            else:
                return 1
        else:
            return 0


    ok_flag = [flag_gen(i) for i in range(len(zh_file_dict))]
    print(np.mean(np.array(ok_flag) > 0))
    print(np.mean(np.array(ok_flag) == 1))
    print(np.mean(np.array(ok_flag) == 2))

    w0_lines = []
    w0_order_dict = []
    w1_lines = []
    w1_order_dict = []
    w2_lines = []
    w2_order_dict = []

    line_k = lambda k: zh_file_dict[k].sub_token + " ||| " + en_file_dict[k].sub_token + "\n"

    for k in range(len(zh_file_dict)):
        if ok_flag[k] == 2:
            w2_lines.append(line_k(k))
            w2_order_dict.append(zh_file_dict[k].sub_order_dict)
        elif ok_flag[k] == 1:
            w1_lines.append(line_k(k))
            w1_order_dict.append(zh_file_dict[k].sub_order_dict)
        else:
            w0_lines.append(line_k(k))
            w0_order_dict.append(zh_file_dict[k].sub_order_dict)
        if k % args.report == args.report - 1:
            print(f"analyzerpool info: generate dict for zh sentence No.{k+1}")

    # use train.dict for the order is mostly the same
    filter_func = lambda k: zh_file_dict[k].sub_order_dict != en_file_dict[k].sub_order_dict and \
                            any([zh_file_dict[k].token_dict[p] != en_file_dict[k].token_dict[p] for p in
                                 zh_file_dict[k].token_dict.keys()])
    order_flag = [filter_func(k) for k in range(len(zh_file_dict)) if ok_flag[k] > 0]
    print("different order percent: %5f" % (sum(order_flag) / len(order_flag)))

    with open(file_path_prefix + ".term_error", "w", encoding="utf8") as w0:
        w0.writelines(w0_lines)
    with open(file_path_prefix + ".term_error.dict", "w", encoding="utf8") as w0_od:
        json.dump(w0_order_dict, w0_od, ensure_ascii=False)

    with open(file_path_prefix + ".term_empty", "w", encoding="utf8") as w1:
        w1.writelines(w1_lines)
    with open(file_path_prefix + ".term_empty.dict", "w", encoding="utf8") as w1_od:
        json.dump(w1_order_dict, w1_od, ensure_ascii=False)

    with open(file_path_prefix + ".term_nonempty", "w", encoding="utf8") as w2:
        w2.writelines(w2_lines)
    with open(file_path_prefix + ".term_nonempty.dict", "w", encoding="utf8") as w2_od:
        json.dump(w2_order_dict, w2_od, ensure_ascii=False)

    assert 1 > 2
