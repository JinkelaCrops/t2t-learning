from concurrent.futures import ThreadPoolExecutor
import json
import re
import os
import pickle

from loginst import logger

class Sync_io(object):
    def __init__(self):
        self.pool_write = ThreadPoolExecutor(max_workers=1)
        self.pool_read = ThreadPoolExecutor(max_workers=1)

    def write(self, *args):
        """
        :param args: (path, {"flag":write_flag, "data":write_data})
        :return:
        """
        # self.with_write(*args)
        self.pool_write.submit(self.with_write, *args)

    def read(self, *args):
        """
        :param args: (path, {"start":read_start, "num":read_num, "end":read_end})
        :return:
        """
        # return self.with_read(*args)
        tmp = self.pool_read.submit(self.with_read, *args)
        return tmp.result()

    @staticmethod
    def with_write(path, write_args):
        write_flag = write_args["flag"]
        write_data = write_args["data"]
        with open(path, write_flag, encoding="utf8") as f:
            f.writelines(write_data)

    @staticmethod
    def with_read(path, read_args):
        read_start = read_args["start"]
        # read_num = read_args["num"]
        # with open(path, "r", encoding="utf8") as f:
        #     line_read = LineRead(f)
        #     read_data = line_read.read_line_by_num(read_start, line_num=read_num)
        # return json.dumps({"result": read_data})
        read_end = read_args["end"]
        with open(path, "r", encoding="utf8") as f:
            line_read = LineRead(f)
            read_data = line_read.read_line_by_end(read_start, stop_pos=read_end)
        return json.dumps({"result": read_data})


def understand_data(data):
    if isinstance(type(data), bytes):
        try:
            data = pickle.loads(data)
        except:
            raise ValueError("Can not pickle bytes!")
    else:
        try:
            data = json.loads(data)
        except:
            pass
    return data


def file_scan(dir_path, recursive=False, showdir=False):
    file_list = []
    if recursive and showdir:
        for fadir, chdir, files in os.walk(dir_path):
            file_list += [os.path.join(fadir, x) for x in chdir]
            file_list += [os.path.join(fadir, x) for x in files]
        return file_list
    elif recursive and not showdir:
        for fadir, chdir, files in os.walk(dir_path):
            if len(files) > 1:
                file_list += [os.path.join(fadir, x) for x in files]
        return file_list
    elif not recursive:
        return [os.path.join(dir_path, x) for x in os.listdir(dir_path)]


def linenum_to_pointer(path, line_num=50):
    pointer_lst = [0]
    with open(path, "rb") as f:
        data = f.read()
    for k, piece in enumerate(re.finditer(b"\n", data)):
        if (k + 1) % line_num == 0:
            pointer_lst.append(piece.end())
    if len(data[pointer_lst[-1]:]) == 0:
        return pointer_lst[:-1]
    else:
        return pointer_lst


def bucket_to_pointer(path, bucket_size=1024):
    pointer_lst = [0]
    with open(path, "rb") as f:
        data = f.read()
    if len(data) == 0:
        return pointer_lst
    p = re.compile(b"\n")
    for i in range((len(data) - 1) // bucket_size + 1):
        m = p.search(data, pos=bucket_size + pointer_lst[-1])
        if m is not None:
            last_pos = m.end()
        else:
            break
        pointer_lst.append(last_pos)
    if len(data[pointer_lst[-1]:]) == 0:
        pointer_lst = pointer_lst[:-1]
    pointer_lst.append(len(data))
    return pointer_lst


class LineRead(object):
    def __init__(self, f):
        self.here = 0
        self.f = f
        self.eof = False

    def read_line_by_num(self, here, line_num=0):
        """
        f = open("./file-down/file-down.log", "r", encoding="utf8")
        line_read = LineRead(f)
        data = line_read.read_line_num(0, line_num=500)
        len(data) == 500
        """
        if line_num == 0:
            raise Exception("do not know how many data to read")
        self.here = here
        self.f.seek(self.here)
        data = []
        count = 0
        while count < line_num:
            line = self.f.readline()
            if line == "":
                self.eof = True
                break
            data.append(line)
            count += 1
        self.here = self.f.tell()
        return data

    def read_line_by_end(self, here, stop_pos=0):
        """
        f = open("./file-down/file-down.log", "r", encoding="utf8")
        line_read = LineRead(f)
        data = line_read.read_line_end(0, stop_pos=47348)
        len(data) == 500
        """
        if stop_pos == 0:
            raise Exception("do not know how many data to read")
        self.here = here
        self.f.seek(self.here)
        data = []
        cupos = 0
        while cupos < stop_pos:
            line = self.f.readline()
            if line == "":
                self.eof = True
                break
            data.append(line)
            cupos = self.f.tell()
        self.here = self.f.tell()
        return data

    # def read(self, here, line_num):
    #     """
    #     f = open("../file-down.log", "r", encoding="utf8")
    #     line_read = LineRead(f)
    #     data, pos = line_read.read(500, 0)
    #     data, pos = line_read.read(500, pos)
    #     data, pos = line_read.read(500, pos)
    #     data, pos = line_read.read(500, pos)
    #     len(data) == 446
    #     """
    #     self.here = here
    #     self.f.seek(self.here)
    #     data = []
    #     for i in range(line_num):
    #         line = self.f.readline()
    #         if line == "":
    #             self.eof = True
    #             break
    #         data.append(line)
    #     self.here = self.f.tell()
    #     return data

    # def read_line(self, read_start, read_nrows):
    #     """
    #
    #     :param f: file flow
    #     :param read_start: start line
    #     :param read_nrows: num of rows
    #     :return:
    #     """
    #     return [line for k, line in enumerate(self.f) if read_start <= k < read_start + read_nrows]


if __name__ == '__main__':
    sync = Sync_io()
    # tmp = sync.write("try2.txt", "w", ["dsd\n", "dsadsda\n", "dasd\n"])
    # print(tmp)
    # pool = ThreadPoolExecutor(max_workers=4)
    #
    #
    # def addd(x, k):
    #     return x + k
    #
    #
    # num = pool.map(lambda args: addd(*args), zip([1, 2], [300, 400]))
    # print(list(num))

    print(sync.read("try2.txt", {"start": 0, "num": 2, "end": 0}))
