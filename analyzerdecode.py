# -*- coding: utf-8 -*-
import json
import re
import argparse

parser = argparse.ArgumentParser(description="analyzerdecode.py")
parser.add_argument('-f', "--file_path")
parser.add_argument('-d', "--dict_path")
parser.add_argument('-t', "--to_file_path")
parser.add_argument('--dict_type', default="raw")

args = parser.parse_args()


def sub_sent(sent, sub_order_dict):
    for rep, target in sub_order_dict:
        m = re.search(rep, sent)
        sent = sent[:m.start()] + target + sent[m.end():] if m is not None else sent
    return sent


def decode_sent(sents, sents_dict):
    bad_sents = []
    zh_decode = []
    for k, (sent, sub_dict) in enumerate(zip(sents, sents_dict)):
        try:
            if len(sub_dict) > 0:
                zh_decode.append(sub_sent(sent, sub_dict))
            else:
                zh_decode.append(sent)
        except Exception as e:
            bad_sents.append([sent, sub_dict])
            zh_decode.append(sent)
    if len(bad_sents) > 0:
        print("decode_sent: warning: bad_sent!")
    return zh_decode


if __name__ == '__main__':
    file_path = args.file_path
    dict_path = args.dict_path
    to_file_path = args.to_file_path

    with open(file_path, "r", encoding="utf8") as f:
        zh = f.readlines()

    if args.dict_type == "raw":
        with open(dict_path, "r", encoding="utf8") as f:
            zh_dict = [json.loads(line[-1]) for line in f.readlines()]
    else:
        with open(dict_path, "r", encoding="utf8") as f:
            zh_dict = json.load(f)

    zh_decode = decode_sent(zh, zh_dict)

    with open(to_file_path, "w", encoding="utf8") as f:
        f.writelines(zh_decode)
