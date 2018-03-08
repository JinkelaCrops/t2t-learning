from concurrent.futures import ThreadPoolExecutor
import json
import re

class Sync_io(object):
    def __init__(self):
        self.pool_write = ThreadPoolExecutor(max_workers=1)
        self.pool_read = ThreadPoolExecutor(max_workers=1)

    def write(self, *args):
        """

        :param args: (path, write_flag, data)
        :return:
        """
        # self.with_write(*args)
        # return 0
        self.pool_write.submit(self.with_write, *args)
        return 0

    def read(self, *args):
        """
        pool.submit do not return result, use map instead
        :param args: (path, read_start, read_nrows)
        :return:
        """
        # return self.with_read(*args)
        tmp = self.pool_read.submit(self.with_read, *args)
        return tmp.result()

    @staticmethod
    def with_write(path, write_flag, data):
        with open(path, write_flag, encoding="utf8") as f:
            f.writelines(data)
        return 0

    @staticmethod
    def with_read(path, read_start, read_nrows, pointer=False):
        with open(path, "r", encoding="utf8") as f:
            line_read = LineRead(f)
            if pointer:
                data = line_read.read(read_start, read_nrows)
            else:
                data = line_read.read_line(read_start, read_nrows)
        tmp = json.dumps({"data": data})
        return tmp


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


def linenum_to_pointer(path, line_num):
    pointer_lst = [0]
    with open(path, "rb") as f:
        data = f.read()
    for k, piece in enumerate(re.finditer(b"\n", data)):
        if (k+1) % line_num == 0:
            pointer_lst.append(piece.span()[1])
    if len(data[pointer_lst[-1]:]) == 0:
        return pointer_lst[:-1]
    else:
        return pointer_lst


class LineRead(object):
    def __init__(self, f):
        self.here = 0
        self.f = f
        self.eof = False

    def read(self, here, line_num):
        """
        f = open("../file-down.log", "r", encoding="utf8")
        line_read = LineRead(f)
        data, pos = line_read.read(500, 0)
        data, pos = line_read.read(500, pos)
        data, pos = line_read.read(500, pos)
        data, pos = line_read.read(500, pos)
        len(data) == 446
        """
        self.here = here
        self.f.seek(self.here)
        data = []
        for i in range(line_num):
            line = self.f.readline()
            if line == "":
                self.eof = True
                break
            data.append(line)
        self.here = self.f.tell()
        return data

    def read_line(self, read_start, read_nrows):
        """

        :param f: file flow
        :param read_start: start line
        :param read_nrows: num of rows
        :return:
        """
        return [line for k, line in enumerate(self.f) if read_start <= k < read_start + read_nrows]


if __name__ == '__main__':
    sync = Sync_io()
    tmp = sync.write("try2.txt", "w", ["dsd\n", "dsadsda\n", "dasd\n"])
    print(tmp)
    pool = ThreadPoolExecutor(max_workers=4)


    def addd(x, k):
        return x + k


    num = pool.map(lambda args: addd(*args), zip([1, 2], [300, 400]))
    print(list(num))

    print(sync.read("try2.txt", 0, 2))