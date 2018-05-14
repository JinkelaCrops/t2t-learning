from utils.datatool import RemoteIO
from concurrent.futures import ProcessPoolExecutor
import time
import os
from utils.simplelog import Logger
from processutils.textfilter import Unpack

import argparse

parser = argparse.ArgumentParser(description="my_merge_unpack")
parser.add_argument('-i', "--input_dir", required=True)
parser.add_argument('-sep', "--separator", required=True)
parser.add_argument('--task_name', default="data")
parser.add_argument("--src_lan", default="lan1")
parser.add_argument("--tgt_lan", default="lan2")
parser.add_argument('--bucket_size', default=30 * 1024 ** 2, type=int)
parser.add_argument('--workers', default=4, type=int)

args = parser.parse_args([
    "-i", "../test/medicine.sample",
    "-sep", ' ||| ',
    "--src_lan", "zh",
    "--tgt_lan", "en",
])
# args = parser.parse_args()
args.output_dir = args.input_dir + ".data"
args.output_src_name = args.task_name + "." + args.src_lan
args.output_tgt_name = args.task_name + "." + args.tgt_lan

remoteio = RemoteIO("localhost")

log = Logger("my_merge_unpack", "my_merge_unpack.log").log()


def submit_task(file_arg_dict):
    file_path = file_arg_dict["file_path"]
    read_start, read_end = file_arg_dict["read_args"]
    data = remoteio.load(file_path, read_start, read_end)

    unpack = Unpack(args.separator)
    zh_lines = []
    en_lines = []

    t0 = time.time()
    for k, line in enumerate(data):
        try:
            zh, en, change_order = unpack.unpack(line)
        except Exception as e:
            log.error(f"unpack error: {e.__class__}, {e.__context__}, ### {line.strip()}")
            continue

        zh_lines.append(zh + "\n")
        en_lines.append(en + "\n")

    time_delta = time.time() - t0
    log.info(f"[submit_task]: spend time: %.2f, speed: %.2f MB/s" % (
        time_delta, (read_end - read_start) / 1024 ** 2 / time_delta))

    write_flag = "a"
    remoteio.save(zh_lines, os.path.join(args.output_dir, args.output_src_name), write_flag)
    remoteio.save(en_lines, os.path.join(args.output_dir, args.output_tgt_name), write_flag)


if __name__ == '__main__':
    remoteio.rm([args.output_dir])
    remoteio.mk([args.output_dir])
    file_paths = remoteio.ls([args.input_dir], recursive=False, showdir=False)
    file_pointers = remoteio.fp(file_paths, bucket_size=args.bucket_size)
    file_args = []
    for file, pointer_locations in file_pointers.items():
        piece_num = len(pointer_locations) - 1
        start_end_list = list(zip(pointer_locations[:-1], pointer_locations[1:]))
        file_args += [{"file_path": f, "read_args": span} for f, span in zip([file] * piece_num, start_end_list)]

    myexecuter = ProcessPoolExecutor(max_workers=args.workers)
    for file_arg_dict in file_args:
        myexecuter.submit(submit_task, file_arg_dict)
