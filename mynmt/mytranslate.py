# #!/usr/bin/tgtv bash
#
# TASK=med_test/cpu/gen
# TMP_DIR=$HOMEPATH/t2t_datagtgt/$TASK
# FILE_NAME=test.small
#
# # unpack if necessary
# #python unpack.py -f $TMP_DIR/$FILE_NAME
#
# # term tgtcode, input: .src output: .src.encode .src.encode.dict
# python analyzertgtcode.py -f $TMP_DIR/$FILE_NAME.src --report 100000
# python analyzertgtcode.py -f $TMP_DIR/$FILE_NAME.tgt --report 100000
#
# # segmtgtt, input: .tgt(src).encode output: seg..tgt(src).encode
# python segmtgtt.py -f $TMP_DIR/$FILE_NAME.tgt.encode -l tgt
# python segmtgtt.py -f $TMP_DIR/$FILE_NAME.src.encode -l src

from textfilterutils import Unpack
from textfilterutils import AfterProcess
from analyzeutils import Token
from analyzeutils import SentTokenInfo
from analyzeutils import decode_sent
from segmentutils import SegmentJieba
from segmentutils import SegmentNLTK
import shutil
import json
import os
import argparse

parser = argparse.ArgumentParser(description="mytranslate.py")

parser.add_argument("--file_path", required=True)
parser.add_argument("--src_lan", default="lan1")
parser.add_argument("--tgt_lan", default="lan2")
parser.add_argument("--report", default=10000, type=int)
parser.add_argument("--cover", default=False, type=bool)

args = parser.parse_args(
    ["--file_path", "/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449/t2t_med/mynmt/data/test/test",
     "--src_lan", "zh",
     "--tgt_lan", "en",
     "--separator", " ||| "])

if_cover = args.cover
sep = args.separator
file_path = args.file_path
file_name = file_path.replace("\\", "/").split("/")[-1]
file_dir = "/".join(file_path.replace("\\", "/").split("/")[:-1])

src_file_name = file_name
src_file_encode_name = src_file_name + ".encode"
src_file_encode_dict_name = src_file_name + ".encode.dict"
src_file_encode_seg_name = src_file_encode_name + ".seg"

segment_dict = {"en": SegmentNLTK, "zh": SegmentJieba}

tgt_file_encode_seg_translate_name = file_name + "." + args.tgt_lan + ".translate"
tgt_file_encode_seg_translate_decode_name = tgt_file_encode_seg_translate_name + ".decode"


def file_analyze():
    if not if_cover:
        if all(os.path.exists(file_dir + "/" + ff) for ff in [src_file_encode_name, src_file_encode_dict_name]):
            print(f"analyze info: {src_file_encode_name} and {src_file_encode_dict_name} exist, exit analyze")
            return 0

    f_name, f_encode_name, f_encode_dict_name = src_file_name, src_file_encode_name, src_file_encode_dict_name
    tokens = Token()
    lines = []
    file_dict = []
    with open(file_dir + "/" + f_name, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            lk = SentTokenInfo(line[:-1])
            lk.execute_token(tokens)
            lines.append(lk.sub_token)
            file_dict.append(lk.sub_order_dict)
            if k % args.report == args.report - 1:
                print(f"analyzerencoder info: execute {f_name} sentence No.{k+1}")

    with open(file_dir + "/" + f_encode_name, "w", encoding="utf8") as w0:
        w0.writelines([x + "\n" for x in lines])
    with open(file_dir + "/" + f_encode_dict_name, "w", encoding="utf8") as w0_od:
        json.dump(file_dict, w0_od, ensure_ascii=False)
    print(f"analyzerencoder info: write down {f_encode_name}, {f_encode_dict_name}")

    return 0


def file_segment():
    if not if_cover:
        if all(os.path.exists(file_dir + "/" + ff) for ff in [src_file_encode_seg_name]):
            print(f"segment info: {src_file_encode_seg_name} exist, exit segment")
            return 0

    f_name, f_seg_name, lan = src_file_encode_name, src_file_encode_seg_name, args.src_lan
    seg_lines = []
    process_class = segment_dict[lan]
    seg_afterprocess_class = AfterProcess
    with open(file_dir + "/" + f_name, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            seg_line = process_class.process(line.strip())
            seg_lines.append(" ".join(seg_line))
            if k % args.report == args.report - 1:
                print(f"segment info: {f_name} segment step {k+1}")

    with open(file_dir + "/" + f_seg_name, "w", encoding="utf8") as f:
        f.writelines([seg_afterprocess_class.afterprocess(line) + "\n" for line in seg_lines])
    return 0


def translate():
    # TODO: wrong
    shutil.copy(file_dir + "/" + src_file_encode_seg_name, file_dir + "/" + tgt_file_encode_seg_translate_name)


def translate_decode():
    f_name = tgt_file_encode_seg_translate_name
    dict_name = src_file_encode_dict_name
    target_name = tgt_file_encode_seg_translate_decode_name

    with open(file_dir + "/" + f_name, "r", encoding="utf8") as f:
        trans = f.readlines()

    with open(file_dir + "/" + dict_name, "r", encoding="utf8") as f:
        src_dict = json.load(f)

    trans_decode_sentences = decode_sent(trans, src_dict)

    with open(file_dir + "/" + target_name, "w", encoding="utf8") as f:
        f.writelines(trans_decode_sentences)


def translate_afterprocess():
    return 0


if __name__ == '__main__':
    # before translate
    file_analyze()
    file_segment()

    # translate
    translate()

    # after translate
    translate_decode()
    translate_afterprocess()
