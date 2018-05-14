from utils.datatool import RemoteIO
from concurrent.futures import ProcessPoolExecutor
import time
import os
from utils.simplelog import Logger
from processutils.textfilter import Unpack

import argparse

parser = argparse.ArgumentParser(description="my_merge")
parser.add_argument('-i', "--input_dir", required=True)
parser.add_argument('-sep', "--separator", required=True)
parser.add_argument('--task_name', default="data")
parser.add_argument('--bucket_size', default=30 * 1024 ** 2, type=int)
parser.add_argument('--workers', default=4, type=int)

args = parser.parse_args([
    "-i", "../test/medicine.sample",
    "-sep", ' ||| ',
])
# args = parser.parse_args()
args.output_dir = args.input_dir + ".data"
args.output_name = args.task_name

remoteio = RemoteIO("localhost")

log = Logger("my_merge", "my_merge.log").log()


def submit_task(file_arg_dict):
    file_path = file_arg_dict["file_path"]
    read_start, read_end = file_arg_dict["read_args"]
    data = remoteio.load(file_path, read_start, read_end)
    write_flag = "a"
    remoteio.save(data, os.path.join(args.output_dir, args.output_name), write_flag)


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
