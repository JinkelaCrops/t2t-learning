# -*- coding: utf-8 -*-
from processutils.analyze import Token
from processutils.analyze import SentTokenInfo
from processutils.textfilter import Unpack
from utils.datatool import RemoteIO
from utils.simplelog import Logger
from concurrent.futures import ProcessPoolExecutor
import time
import json

import argparse
myself = __file__.replace("\\", "/").split("/")[-1]

parser = argparse.ArgumentParser(description=myself)
parser.add_argument('-f', "--file_path")
parser.add_argument('-s', "--separator", default="\t")
parser.add_argument('--file_process_size', default=5000, type=int)
parser.add_argument('--workers', default=4, type=int)

# args = parser.parse_args(["-f", "/media/yanpan/7D4CF1590195F939/Projects/t2t_med/t2t_datagen/med/medicine.txt", "-s", ' ||| '])
args = parser.parse_args()

remoteio = RemoteIO("localhost")

log = Logger(myself, myself.replace(".py", ".log")).log("C")

def main(pointer_position):
    data = remoteio.load(args.file_path, pointer_position, args.file_process_size, 1)

    tokens = Token(False)
    unpack = Unpack(args.separator)
    zh_lines = []
    en_lines = []
    zh_file_dict = []
    en_file_dict = []
    origin_lines = []

    t0 = time.time()
    for k, line in enumerate(data):
        try:
            zh, en, change_order = unpack.unpack(line)
        except Exception as e:
            log.error(f"unpack error: {e.__class__}, {e.__context__}, ### {line.strip()}")
            continue
        zhlk = SentTokenInfo(zh)
        zhlk.execute_token(tokens)
        zh_lines.append(zhlk.sub_token)
        zh_file_dict.append(json.dumps(zhlk.sub_order_dict, ensure_ascii=False))

        enlk = SentTokenInfo(en)
        enlk.execute_token(tokens)
        en_lines.append(enlk.sub_token)
        en_file_dict.append(json.dumps(enlk.sub_order_dict, ensure_ascii=False))

        origin_lines.append(line)

    time_delta = time.time() - t0
    log.info(
        f"analyzerencoder info: spend time: {round(time_delta, 2)}, speed: {int(args.file_process_size/time_delta)} lines/s")

    zh_lines = ["%s\n" % x for x in zh_lines]
    en_lines = ["%s\n" % x for x in en_lines]
    zh_file_dict = ["%s\n" % x for x in zh_file_dict]
    en_file_dict = ["%s\n" % x for x in en_file_dict]

    write_flag = "a"
    remoteio.save(json.dumps(zh_lines), args.file_path + ".zh.encode", write_flag)
    remoteio.save(json.dumps(en_lines), args.file_path + ".en.encode", write_flag)
    remoteio.save(json.dumps(zh_file_dict), args.file_path + ".zh.encode.dict", write_flag)
    remoteio.save(json.dumps(en_file_dict), args.file_path + ".en.encode.dict", write_flag)
    remoteio.save(json.dumps(origin_lines), args.file_path + ".origin", write_flag)

    return 0


if __name__ == '__main__':
    file_pointers = remoteio.exec(f'file_pointers = linenum_to_pointer("{args.file_path}", {args.file_process_size})',
                                  "file_pointers")

    myexecuter = ProcessPoolExecutor(max_workers=args.workers)
    for fp in file_pointers:
        myexecuter.submit(main, fp)
