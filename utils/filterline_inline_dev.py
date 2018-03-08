from robots import Base
from robots import Sepautosplit
from robots import Clean
from robots import Htmlsub
from robots import Hantsub
from robots import Regsub
from robots import Messyrecognize
from robots import Afterprocess
from robots import Ruleprint

from utils.datatool import RemoteIO
from utils.simple_tools import Logger

import re
import os
import json
import time

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import argparse
from common import opts


def make_args(myself):
    parser = argparse.ArgumentParser(
        description=myself,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    opts.add_md_help_argument(parser)
    opts.data_opts(parser)
    opts.preprocess_opts(parser)

    # opt = parser.parse_args(["-i", "/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449/test-data", "-sep", " ||| "])
    opt = parser.parse_args(["-i", "D:/tmxmall-code/text-filter/data/medicine-sample",
                             "-sep", " ||| ",
                             "-multi_process", "True",
                             "-file_process_size", "5000",
                             "-workers", "2"])
    # opt = parser.parse_args()
    # opt.sep = " ||| "

    opt.correct_dir = opt.input_dir + ".correct"
    opt.wrong_dir = opt.input_dir + ".wrong"
    opt.log_dir = opt.input_dir + ".log"
    return opt


class Unpack(Base):
    def __init__(self, sep):
        self.sep = sep
        self.bisentence = ""
        self.auto = Sepautosplit(sep)

    def whichzh(self, zh, en):
        if self.zhratio(zh) < self.zhratio(en):
            return en, zh, True
        else:
            return zh, en, False

    def unpack(self, bisentence):

        self.bisentence = bisentence[:-1]  # get rid of \n
        if len(re.findall("\u0000", self.bisentence.replace(self.sep, "\u0000"))) > 1:
            zh, en = self.auto.sep_auto_detect(self.bisentence)
        else:
            zh, en = self.bisentence.split(self.sep)
        zh, en, change_order = self.whichzh(zh, en)
        return zh, en, change_order


class Pack(Base):
    def __init__(self, sep):
        self.sep = sep
        self.zh_sentence = ""
        self.en_sentence = ""

    def pack(self, zh_sentence, en_sentence, change_order):
        if change_order:
            self.zh_sentence = en_sentence
            self.en_sentence = zh_sentence
        else:
            self.zh_sentence = zh_sentence
            self.en_sentence = en_sentence
        bisentence = self.sep.join([self.zh_sentence, self.en_sentence])
        return bisentence


def process(zh, en, class_set, iflog=False):
    """

    :return:
    """
    zh = class_set.clean.clean(zh)
    en = class_set.clean.clean(en)

    zh = class_set.htmlsub.htmlsub(zh)
    en = class_set.htmlsub.htmlsub(en)

    zh = class_set.hantsub.hantsub(zh)
    en = class_set.hantsub.hantsub(en)

    zh, en = class_set.regsub.regsub(zh, en)

    wrong_flag = class_set.messyrecognize.recognize(zh) | class_set.messyrecognize.recognize(en)

    zh = class_set.afterprocess.process(zh)
    en = class_set.afterprocess.process(en)

    if iflog:
        log_line = class_set.ruleprint.rules(zh, en)

        log_line = log_line + "\n\n" if len(log_line) > 0 else ""
        return zh, en, wrong_flag, log_line
    else:
        return zh, en, wrong_flag


def main(input, filename, index, opt):
    unpack = Unpack(opt.sep)
    pack = Pack(opt.sep)

    class_set = Base()
    class_set.clean = Clean()
    class_set.htmlsub = Htmlsub()
    class_set.hantsub = Hantsub()
    class_set.regsub = Regsub()
    class_set.messyrecognize = Messyrecognize()
    class_set.afterprocess = Afterprocess()
    class_set.ruleprint = Ruleprint()

    input_tmp = []
    log.info("main: unpack start")
    unpack_wrong_num = 0
    unpack_wrong = []
    for bisen in input:
        try:
            assert len(bisen) < opt.max_line_length
            input_tmp.append(unpack.unpack(bisen))
        except:
            unpack_wrong_num += 1
            unpack_wrong.append(bisen)

    good_lines = []
    wrong_lines = []
    log_lines = []

    for zh, en, change_order in input_tmp:
        if opt.log:
            zh, en, wrong_flag, log_line = process(zh, en, class_set, True)
            log_lines.append(log_line)
        else:
            zh, en, wrong_flag = process(zh, en, class_set)

        line = pack.pack(zh, en, change_order)

        if wrong_flag:
            wrong_lines.append("%s\n" % line)
        else:
            good_lines.append("%s\n" % line)

    wrong_lines = unpack_wrong + wrong_lines

    wrong_num = len(wrong_lines)
    wrong_percent = wrong_num / (wrong_num + len(good_lines))
    log.info(
        "main: done %s piece %s, with wrong number: %s, wrong percent: %s" % (
            filename, index, wrong_num, wrong_percent))

    if opt.log:
        return good_lines, wrong_lines, log_lines
    else:
        return good_lines, wrong_lines


def submit_task(arg, opt):
    """
    must make input in each process!
    :param filename: name of file
    :param pieceindex: index of file piece
    :return:
    """
    filename, pieceindex, read_start, pointer = arg
    try:
        input = remoteio.load("%s/%s" % (opt.input_dir, filename), read_start, opt.file_process_size, pointer)
    except Exception as e:
        log.warn("submit_task: remoteio load data 'input' failed: %s:%s" % (e.__class__, e.__context__))
        return None

    t0 = time.time()
    output = main(input, filename, pieceindex, opt)
    line_num = len(output[0]) + len(output[1])
    time_delta = time.time() - t0
    log.info("submit_task: spend time: %s, speed: %s line/s" % (round(time_delta, 2), int(line_num / time_delta)))

    write_flag = "a"
    try:
        remoteio.save(json.dumps(output[0]), "%s/%s" % (opt.correct_dir, filename), write_flag)
    except Exception as e:
        log.warn("submit_task: remoteio save data 'output[0]' failed: %s:%s" % (e.__class__, e.__context__))

    try:
        remoteio.save(json.dumps(output[1]), "%s/%s" % (opt.wrong_dir, filename), write_flag)
    except Exception as e:
        log.warn("submit_task: remoteio save data 'output[1]' failed: %s:%s" % (e.__class__, e.__context__))

    if opt.log:
        try:
            remoteio.save(json.dumps(output[2]), "%s/%s" % (opt.log_dir, filename), write_flag)
        except Exception as e:
            log.warn("submit_task: remoteio save data 'output[2]' failed: %s:%s" % (e.__class__, e.__context__))
    return 0


remoteio = RemoteIO("localhost")

myself = __file__.replace("\\", "/").split("/")[-1]
log = Logger(myself, myself.replace(".py", ".log")).log()
opt = make_args(myself)

if __name__ == "__main__":

    log.info("__main__: split file")

    remoteio.exec('import shutil; shutil.rmtree("%s") if os.path.exists("%s") else None; _ = os.makedirs("%s")' % (
        opt.correct_dir, opt.correct_dir, opt.correct_dir), "_")
    remoteio.exec('import shutil; shutil.rmtree("%s") if os.path.exists("%s") else None; _ = os.makedirs("%s")' % (
        opt.wrong_dir, opt.wrong_dir, opt.wrong_dir), "_")
    if opt.log:
        remoteio.exec('import shutil; shutil.rmtree("%s") if os.path.exists("%s") else None; _ = os.makedirs("%s")' % (
            opt.log_dir, opt.log_dir, opt.log_dir), "_")

    fileargs = []

    file_pointers = remoteio.exec('filenames = list(filter(lambda x:x.endswith(".txt"),os.listdir("%s"))); '
                                  'file_pointers = dict(zip(filenames, list(map(lambda x:linenum_to_pointer("%s/" + x, %s), filenames))))'
                                  % (opt.input_dir, opt.input_dir, opt.file_process_size), "file_pointers")
    for file, pointer_locations in file_pointers.items():
        filename = file.split("/")[-1]
        piecenum = len(pointer_locations)
        fileargs += list(zip([filename] * piecenum, range(piecenum), pointer_locations, [1] * piecenum))

    # filenames = remoteio.exec('filenames = list(filter(lambda x:x.endswith(".txt"),os.listdir("%s"))); '
    #                           'filenames = list(map(lambda x:list(os.popen("wc -l %s/" + x))[0], filenames))' % (
    #                               input_dir, input_dir), "filenames")
    # # filenames = ["20000 D:/tmxmall-code/text-filter/data/medicine-sample/medicine.sample.txt"]
    # for file in filenames:
    #     linenum, filename = file.split()
    #     filename = filename.split("/")[-1]
    #     linenum = int(linenum)
    #     piecenum = int(np.ceil(linenum / SIZEOFFILE))
    #     fileargs += list(zip([filename] * piecenum, range(piecenum), [p * SIZEOFFILE for p in range(piecenum)], [0] * piecenum))

    log.info("__main__: %s" % json.dumps(fileargs))
    if opt.multi_process:
        myexecutor = ProcessPoolExecutor(max_workers=opt.workers)
        for k, filearg in enumerate(fileargs):
            try:
                result = myexecutor.submit(submit_task, filearg, opt)  # result.result()
            except Exception as e:
                log.warn("__main__: processpool submit %s error: %s:%s" % (k, e.__class__, e.__context__))

    else:
        pools = [submit_task(filearg, opt) for filearg in fileargs]

    # myexecutor = ProcessPoolExecutor(max_workers=WORKERS)
    #
    # for i in range(int(np.ceil(len(fileargs) / SIZEOFCHUNK))):
    #     log.info("__main__: processpool chunk %s" % i)
    #     fileargschunk = fileargs[i * SIZEOFCHUNK:(i + 1) * SIZEOFCHUNK]
    #     if MULTIPROCESS:
    #         results = myexecutor.map(submit_task, fileargschunk)
    #
    #         # for k, result in enumerate(results):
    #         #     try:
    #         #         submit_task_write(result)
    #         #     except Exception as e:
    #         #         log.warn("__main__: processpool submit and write %s error: %s:%s" % (k, e.__class__, e.__context__))
    #
    #     else:
    #         # none multiprocess submit_task_write()
    #         pools = [submit_task(filearg) for filearg in fileargschunk]
