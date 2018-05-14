from processutils.analyze import Token
from processutils.analyze import SentTokenInfo
from processutils.wordcountutils import word_count
from processutils.textfilter import Unpack
from processutils.textfilter import RawFilter
from utils.datatool import RemoteIO
from concurrent.futures import ProcessPoolExecutor
import time
import json
import os
from utils.simplelog import Logger

import argparse

parser = argparse.ArgumentParser(description="my_filter")
parser.add_argument('-f', "--file_prefix", required=True)
parser.add_argument('-sep', "--separator", required=True)
parser.add_argument('--bucket_size', default=30 * 1024 ** 2, type=int)
parser.add_argument('--workers', default=4, type=int)

# args = parser.parse_args([
#     "-f", "../test/medicine.sample.data/data.data",
#     "-sep", ' ||| '
# ])
args = parser.parse_args()
args.input_dir = "/".join(args.file_prefix.split("/")[:-1])
args.file_name = args.file_prefix.split("/")[-1]
args.output_dir = args.input_dir + ".filter"

remoteio = RemoteIO("localhost")

log = Logger("my_filter", "my_filter.log").log()


class Field:
    def __init__(self, line, src, tgt):
        self.line = line
        self.src = src
        self.tgt = tgt
        self.src_encode = ""
        self.tgt_encode = ""
        self.src_encode_dict = None
        self.tgt_encode_dict = None


class AnalyzeFilter(object):
    def __init__(self):
        pass

    def sub_order_dict_equal(self, field: Field):
        if field.src_encode_dict == field.tgt_encode_dict:
            if len(field.src_encode_dict) > 0:
                return 2
            else:
                return 1
        else:
            return 0

    def all_term_filter(self, field: Field):
        tgt_count = word_count(field.tgt)
        src_count = word_count(field.src)
        return tgt_count * 0.5 > len(field.tgt_encode_dict) and src_count * 0.5 > len(field.src_encode_dict)

    def raw_filter(self, field: Field):
        flag = RawFilter.tridots_filter(field.src, field.tgt) or RawFilter.clear_filter(field.src, field.tgt)
        return not flag

    def filter(self, field: Field):
        return self.sub_order_dict_equal(field) and self.all_term_filter(field) and self.raw_filter(field)


def submit_task(file_arg_dict):
    file_path = file_arg_dict["file_path"]
    read_start, read_tgtd = file_arg_dict["read_args"]
    data = remoteio.load(file_path, read_start, read_tgtd)
    tokens = Token()
    unpack = Unpack(args.separator)
    analyze_filter = AnalyzeFilter()

    fields = []
    t0 = time.time()
    for k, line in enumerate(data):
        try:
            src, tgt, change_order = unpack.unpack(line)
        except Exception as e:
            log.error(f"unpack error: {e.__class__}, {e.__context__}, ### {line.strip()}")
            continue
        field = Field(line, src, tgt)

        srclk = SentTokenInfo(field.src)
        srclk.execute_token(tokens)
        field.src_encode = srclk.sub_token
        field.src_encode_dict = srclk.sub_order_dict

        tgtlk = SentTokenInfo(field.tgt)
        tgtlk.execute_token(tokens)
        field.tgt_encode = tgtlk.sub_token
        field.tgt_encode_dict = tgtlk.sub_order_dict

        if analyze_filter.filter(field):
            fields.append(field)

    time_delta = time.time() - t0
    log.info(f"[submit_task]: spend time: %.2f, speed: %.2f MB/s" % (
        time_delta, (read_tgtd - read_start) / 1024 ** 2 / time_delta))

    origin_lines = [field.line for field in fields]
    src_lines = [field.src_encode + "\n" for field in fields]
    tgt_lines = [field.tgt_encode + "\n" for field in fields]
    src_file_dict = [json.dumps(field.src_encode_dict, ensure_ascii=False) + "\n" for field in fields]
    tgt_file_dict = [json.dumps(field.tgt_encode_dict, ensure_ascii=False) + "\n" for field in fields]

    write_flag = "a"
    remoteio.save(src_lines, os.path.join(args.output_dir, args.file_name + ".src.encode"), write_flag)
    remoteio.save(tgt_lines, os.path.join(args.output_dir, args.file_name + ".tgt.encode"), write_flag)
    remoteio.save(src_file_dict, os.path.join(args.output_dir, args.file_name + ".src.encode.dict"), write_flag)
    remoteio.save(tgt_file_dict, os.path.join(args.output_dir, args.file_name + ".tgt.encode.dict"), write_flag)
    remoteio.save(origin_lines, os.path.join(args.output_dir, args.file_name + ".origin"), write_flag)
    return 0


if __name__ == '__main__':
    remoteio.rm([args.output_dir])
    remoteio.mk([args.output_dir])
    file_pointers = remoteio.fp([args.file_prefix], bucket_size=args.bucket_size)
    file_args = []
    for file, pointer_locations in file_pointers.items():
        piece_num = len(pointer_locations) - 1
        start_end_list = list(zip(pointer_locations[:-1], pointer_locations[1:]))
        file_args += [{"file_path": f, "read_args": span} for f, span in zip([file] * piece_num, start_end_list)]

    if args.workers:
        myexecuter = ProcessPoolExecutor(max_workers=args.workers)
        for file_arg_dict in file_args:
            myexecuter.submit(submit_task, file_arg_dict)
    else:
        [submit_task(file_arg_dict) for file_arg_dict in file_args]
