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
from analyzeutils import sub_sent
from segmentutils import SegmentJieba
from segmentutils import SegmentNLTK
import argparse

parser = argparse.ArgumentParser(description="mytranslate_eval_inline.py")

parser.add_argument("--file_path", required=True)
parser.add_argument("--src_lan", default="lan1")
parser.add_argument("--tgt_lan", default="lan2")
parser.add_argument("--separator", default="\t")
parser.add_argument("--report", default=10000, type=int)

args = parser.parse_args()

sep = args.separator
src_lan = args.src_lan
tgt_lan = args.tgt_lan
file_path = args.file_path
file_name = file_path.replace("\\", "/").split("/")[-1]
file_dir = "/".join(file_path.replace("\\", "/").split("/")[:-1])

segment_dict = {"en": SegmentNLTK, "zh": SegmentJieba}
target_file_name = file_name + "." + tgt_lan + ".translate"


def translate_one(x0, x1):
    return x1


def translate_afterprocess(line):
    return line


def bleu(tgt, trans):
    return 0


def decode_inline(line):
    # unpack
    unpack = Unpack(sep)
    try:
        src, tgt, change_order = unpack.unpack(line.strip())
    except Exception as e:
        print(f"unpack error: {e.__class__}, {e.__context__}, ### {line.strip()}")
        return None

    # analyze
    tokens = Token()
    src_lk = SentTokenInfo(src)
    src_lk.execute_token(tokens)
    src_encode = src_lk.sub_token
    src_encode_dict = src_lk.sub_order_dict
    tgt_lk = SentTokenInfo(tgt)
    tgt_lk.execute_token(tokens)
    tgt_encode = tgt_lk.sub_token

    # segment
    seg_afterprocess_class = AfterProcess
    src_process_class = segment_dict[src_lan]
    src_encode_seg = src_process_class.process(src_encode)
    src_encode_seg = seg_afterprocess_class.afterprocess(" ".join(src_encode_seg))
    tgt_process_class = segment_dict[tgt_lan]
    tgt_encode_seg = tgt_process_class.process(tgt_encode)
    tgt_encode_seg = seg_afterprocess_class.afterprocess(" ".join(tgt_encode_seg))

    # translate
    tgt_encode_seg_translate = translate_one(src_encode_seg, tgt_encode_seg)  # here is wrong, no tgt_encode_seg

    # translate decode
    try:
        tgt_encode_seg_translate_decode = sub_sent(tgt_encode_seg_translate, src_encode_dict)
    except Exception as e:
        print(f"translate decode error: {e.__class__}, {e.__context__}, ### {line.strip()}")
        return None

    # translate afterprocess
    trans = translate_afterprocess(tgt_encode_seg_translate_decode)

    return src, tgt, trans


if __name__ == '__main__':
    with open(file_path, "r", encoding="utf8") as f:
        data = f.readlines()

    output = []
    for k, line in enumerate(data):
        line_src, line_tgt, line_trans = decode_inline(line)
        output.append(line_trans)
        if k % args.report == args.report - 1:
            print(f"execute {f_name} sentence No.{k+1}")

    with open(file_dir + "/" + target_file_name, "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in output])
