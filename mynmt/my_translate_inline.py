from processutils.analyze import Token
from processutils.analyze import SentTokenInfo
from processutils.analyze import sub_sent
from processutils.analyze import translate_afterprocess
from processutils.segment import SegmentJieba
from processutils.segment import SegmentNLTK
from processutils.segment import segment_afterprocess
from mynmt.my_t2t_decoder import SessFieldPredict
from mynmt.my_t2t_decoder import decode
import mynmt.my_config as config
import re
import argparse
from utils.simplelog import Logger

parser = argparse.ArgumentParser(description="my_translate_inline.py")
logger = Logger("my_translate_inline", "my_translate_inline.log").log("F")

parser.add_argument("--file_path", required=True)
parser.add_argument("--src_lan", default="lan1")
parser.add_argument("--tgt_lan", default="lan2")
parser.add_argument("--report", default=10000, type=int)
parser.add_argument("--truncate", default=1E10, type=int)

args = parser.parse_args([
    "--file_path", "../test/medicine.sample.data/data.test.src",
    "--src_lan", "zh",
    "--tgt_lan", "en",
    "--truncate", "500"
])

src_lan = args.src_lan
tgt_lan = args.tgt_lan
file_path = args.file_path
file_name = file_path.replace("\\", "/").split("/")[-1]
file_dir = "/".join(file_path.replace("\\", "/").split("/")[:-1])

segment_dict = {"en": SegmentNLTK, "zh": SegmentJieba}
target_file_name = file_name + "." + tgt_lan + ".translate"

tokens = Token()
trans_after_regex = "(" + "|".join(tokens.get_token_name) + ")"

sess_field = SessFieldPredict(config)


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


def translate_one(fields: list):
    inputs = [field.src_encode_seg for field in fields]
    outputs = decode(inputs, sess_field)
    for i in range(len(fields)):
        fields[i].tgt_encode_seg_translate = outputs[i]


def before_translate(fields: list):
    for i in range(len(fields)):
        # unpack
        src = fields[i].src.strip()

        # analyze
        fields[i].trans_after_regex = trans_after_regex
        src_lk = SentTokenInfo(src)
        src_lk.execute_token(tokens)
        fields[i].src_encode = src_lk.sub_token
        fields[i].src_encode_dict = src_lk.sub_order_dict

        # segment
        src_process_class = segment_dict[fields[i].src_lan]
        src_encode_seg = src_process_class.process(fields[i].src_encode)
        fields[i].src_encode_seg = segment_afterprocess(" ".join(src_encode_seg))


def after_translate(fields: list):
    for i in range(len(fields)):
        # translate decode
        try:
            fields[i].tgt_encode_seg_translate_decode = sub_sent(fields[i].tgt_encode_seg_translate,
                                                                 fields[i].src_encode_dict)
        except Exception as e:
            logger.warn(f"translate decode error: {e.__class__}, {e.__context__}, ### {line.strip()}")
        fields[i].backup_decode()

        # translate afterprocess
        fields[i].trans = translate_afterprocess(fields[i].tgt_encode_seg_translate_decode)


def decode_inline(line_batch):
    fields = [Field(line, src_lan) for line in line_batch]
    before_translate(fields)
    translate_one(fields)
    after_translate(fields)
    return [field.src for field in fields], [field.trans for field in fields]


if __name__ == '__main__':
    with open(file_path, "r", encoding="utf8") as f:
        data = f.readlines()[:args.truncate]
    assert len(data) > 0

    output = []
    num_of_batch = (len(data) - 1) // sess_field.batch_size + 1
    for k in range(num_of_batch):
        lines = data[k * sess_field.batch_size: (k + 1) * sess_field.batch_size]
        src_lines, trans_lines = decode_inline(lines)
        output += trans_lines
        if k % args.report == args.report - 1:
            logger.info(f"execute {file_name} sentence No.{(k + 1) * sess_field.batch_size}")

    with open(file_dir + "/" + target_file_name, "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in output])
