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

from analyzeutils import Token
from analyzeutils import SentTokenInfo
from analyzeutils import segment_afterprocess
from analyzeutils import sub_sent
from analyzeutils import translate_afterprocess
from segmentutils import SegmentJieba
from segmentutils import SegmentNLTK
# from tensor2tensor.bin import t2t_decoder
import re
import argparse

parser = argparse.ArgumentParser(description="mytranslate_inline.py")

parser.add_argument("--file_path", required=True)
parser.add_argument("--src_lan", default="lan1")
parser.add_argument("--tgt_lan", default="lan2")
parser.add_argument("--report", default=10000, type=int)

args = parser.parse_args(
    ["--file_path", "../test/test.en",
     "--src_lan", "en",
     "--tgt_lan", "zh"])

src_lan = args.src_lan
tgt_lan = args.tgt_lan
file_path = args.file_path
file_name = file_path.replace("\\", "/").split("/")[-1]
file_dir = "/".join(file_path.replace("\\", "/").split("/")[:-1])

segment_dict = {"en": SegmentNLTK, "zh": SegmentJieba}
target_file_name = file_name + "." + tgt_lan + ".translate"

tokens = Token()
trans_after_regex = "(" + "|".join(tokens.get_token_name) + ")"


class Field(object):
    def __init__(self, src, src_lan):
        self.src = src
        self.src_lan = src_lan
        self.src_encode = ""
        self.src_encode_dict = []
        self.src_encode_seg = ""
        self.trans_after_regex = ""
        self.tgt_encode_seg_translate = ""
        self.tgt_encode_seg_translate_decode = ""
        self.trans = ""

    def backup_decode(self):
        if self.trans_after_regex:
            self.tgt_encode_seg_translate_decode = re.sub(self.trans_after_regex, "", self.tgt_encode_seg_translate)
        else:
            self.tgt_encode_seg_translate_decode = self.tgt_encode_seg_translate


def translate_one(field: Field):
    field.tgt_encode_seg_translate = field.src_encode_seg


def before_translate(field: Field):
    # unpack
    src = field.src.strip()

    # analyze
    field.trans_after_regex = trans_after_regex
    src_lk = SentTokenInfo(src)
    src_lk.execute_token(tokens)
    field.src_encode = src_lk.sub_token
    field.src_encode_dict = src_lk.sub_order_dict

    # segment
    src_process_class = segment_dict[field.src_lan]
    src_encode_seg = src_process_class.process(field.src_encode)
    field.src_encode_seg = segment_afterprocess(" ".join(src_encode_seg))


def after_translate(field: Field):
    # translate decode
    try:
        field.tgt_encode_seg_translate_decode = sub_sent(field.tgt_encode_seg_translate, field.src_encode_dict)
    except Exception as e:
        print(f"translate decode error: {e.__class__}, {e.__context__}, ### {line.strip()}")
        field.backup_decode()

    # translate afterprocess
    field.trans = translate_afterprocess(field.tgt_encode_seg_translate_decode)


def decode_inline(line):
    field = Field(line, src_lan)
    before_translate(field)
    translate_one(field)
    after_translate(field)
    return field.src, field.trans


if __name__ == '__main__':
    with open(file_path, "r", encoding="utf8") as f:
        data = f.readlines()

    output = []
    for k, line in enumerate(data):
        src, tgt_trans = decode_inline(line)
        output.append(tgt_trans)
        if k % args.report == args.report - 1:
            print(f"execute {file_name} sentence No.{k+1}")

    with open(file_dir + "/" + target_file_name, "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in output])
