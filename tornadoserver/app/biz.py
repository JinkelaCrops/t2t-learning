from processutils.analyze import Token
from processutils.analyze import SentTokenInfo
from processutils.analyze import sub_sent
from processutils.analyze import translate_afterprocess
from processutils.segment import SegmentJieba
from processutils.segment import SegmentNLTK
from processutils.segment import segment_afterprocess
from mynmt.my_t2t_decoder import decode
from mynmt.my_t2t_decoder import SessFieldPredict
import tornadoserver.config as config
import re

from tornadoserver.loginst import logger

src_lan = config.SRC_LAN
tgt_lan = config.TGT_LAN
segment_dict = {"en": SegmentNLTK, "zh": SegmentJieba}
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

