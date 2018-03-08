# -*- coding: utf-8 -*-
import json
import re
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="analyzerfilter.py")
parser.add_argument('-f', "--file_path")
parser.add_argument('-zhf', "--file_path_zh")
parser.add_argument('-enf', "--file_path_en")
parser.add_argument('-zhd', "--dict_path_zh")
parser.add_argument('-end', "--dict_path_en")

# args = parser.parse_args("-f ../t2t_med/t2t_datagen/med/medicine.txt.origin -zhf ../t2t_med/t2t_datagen/med/medicine.txt.zh.encode -enf ../t2t_med/t2t_datagen/med/medicine.txt.en.encode -zhd ../t2t_med/t2t_datagen/med/medicine.txt.zh.encode.dict -end ../t2t_med/t2t_datagen/med/medicine.txt.en.encode.dict".split())
args = parser.parse_args()


def sub_order_dict_equal(dict_a, dict_b):
    dict_a_tmp = [(term[0], re.sub(" ", "", term[1])) for term in json.loads(dict_a[:-1])]
    dict_b_tmp = [(term[0], re.sub(" ", "", term[1])) for term in json.loads(dict_b[:-1])]
    if dict_a_tmp == dict_b_tmp:
        if len(dict_a_tmp) > 0:
            return 2
        else:
            return 1
    else:
        return 0


if __name__ == '__main__':
    with open(args.file_path_zh, "r", encoding="utf8") as f:
        zh = f.readlines()
    with open(args.dict_path_zh, "r", encoding="utf8") as f:
        zh_dict = f.readlines()

    with open(args.file_path_en, "r", encoding="utf8") as f:
        en = f.readlines()
    with open(args.dict_path_en, "r", encoding="utf8") as f:
        en_dict = f.readlines()

    ok_flag = [sub_order_dict_equal(i, j) for i, j in zip(zh_dict, en_dict)]
    print("analyzerfilter info: same term sentence frac:", np.mean(np.array(ok_flag) > 0))
    print("analyzerfilter info: none term sentence frac:", np.mean(np.array(ok_flag) == 1))
    print("analyzerfilter info: with term sentence frac:", np.mean(np.array(ok_flag) == 2))

    term_zh = [line for k, line in enumerate(zh) if ok_flag[k] > 0]
    term_en = [line for k, line in enumerate(en) if ok_flag[k] > 0]
    term_zh_dict = [line for k, line in enumerate(zh_dict) if ok_flag[k] > 0]
    term_en_dict = [line for k, line in enumerate(en_dict) if ok_flag[k] > 0]

    with open(args.file_path_zh + ".term_filter", "w", encoding="utf8") as w0:
        w0.writelines(term_zh)
    with open(args.dict_path_zh + ".term_filter", "w", encoding="utf8") as w0_od:
        w0_od.writelines(term_zh_dict)

    with open(args.file_path_en + ".term_filter", "w", encoding="utf8") as w1:
        w1.writelines(term_en)
    with open(args.dict_path_en + ".term_filter", "w", encoding="utf8") as w1_od:
        w1_od.writelines(term_en_dict)

    del zh, en, zh_dict, en_dict, term_zh, term_en, term_zh_dict, term_en_dict

    with open(args.file_path, "r", encoding="utf8") as f:
        data = f.readlines()
    term_data = [line for k, line in enumerate(data) if ok_flag[k] > 0]
    with open(args.file_path + ".term_filter", "w", encoding="utf8") as f:
        f.writelines(term_data)
