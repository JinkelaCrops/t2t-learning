# -*-coding: utf-8 -*-
# __author__ : tinytiger
# __time__   : '2018/1/4 11:08'

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.
import tornado.web
import pickle
import json
import sys
import os

from app.simplelog import Logger
from app.biz import understand_data
from app.biz import linenum_to_pointer
from app.biz import Sync_io

log = Logger("file-down", "file-down.log").log("F")
sync_io = Sync_io()


class WriteDownHandler(tornado.web.RequestHandler):

    def decode_argument(self, value, name=None):
        from tornado.escape import _unicode
        from tornado.web import HTTPError
        try:
            return _unicode(value)
        except UnicodeDecodeError:
            return bytes(value)
        except:
            raise HTTPError(400, "Invalid unicode or bytes in %s: %r" %
                            (name or "url", value[:40]))

    def post(self):
        log.info("WriteDownHandler.post: get data from memory")
        data = self.get_argument("data")
        data = understand_data(data)
        log.info("WriteDownHandler.post: got data")

        file_name = self.get_argument("file_name")
        if not isinstance(file_name, str):
            log.warn("WriteDownHandler.post: TypeError: file_name is not string")
            return

        # path = data_dir % file_name
        path = file_name
        write_flag = self.get_argument("write_mode")
        if not isinstance(write_flag, str):
            log.warn("WriteDownHandler.post: TypeError: write_flag is not string")
            return

        log.info("WriteDownHandler.post: write data into %s" % path)

        # with open(path, write_flag, encoding="utf8") as f:
        #     f.writelines(data)

        sync_io.write(path, write_flag, data)
        log.info("WriteDownHandler.post: wrote done")


class SendOutHandler(tornado.web.RequestHandler):

    def post(self):
        file_name = self.get_argument("file_name")
        if not isinstance(file_name, str):
            log.warn("SendOutHandler.post: TypeError: file_name is not string")
            return

        # path = data_dir % file_name
        path = file_name
        read_start = int(self.get_argument("read_start"))
        read_nrows = int(self.get_argument("read_nrows"))
        pointer = int(self.get_argument("pointer"))

        if pointer:
            log.info("SendOutHandler.post: send data from %s [%s] -> %s" % (path, read_start, read_nrows))
        else:
            log.info("SendOutHandler.post: send data from %s [%s : %s]" % (path, read_start, read_start + read_nrows))

        # with open(path, "r", encoding="utf8") as f:
        #     tmp = json.dumps({"data": line_read(f, read_start, read_nrows)})
        # self.write(tmp)

        self.write(sync_io.read(path, read_start, read_nrows, pointer))
        log.info("SendOutHandler.post: sent data")


class ExecHandler(tornado.web.RequestHandler):

    def post(self):
        python_code = self.get_argument("python_code")
        result_name = self.get_argument("result_name")
        if not isinstance(python_code, str):
            log.warn("TypeError: python_code is not string")
            return
        if not isinstance(result_name, str):
            log.warn("TypeError: result_name is not string")
            return

        log.info("execute python code: %s" % python_code)
        # before_exec = list(vars().keys())
        # exec(python_code)
        # after_exec = list(vars().keys())
        # tmp_vars = list(filter(lambda x: not x.startswith("_"), set(after_exec) - set(before_exec)))
        # self.write(json.dumps({"result": vars()[tmp_vars[0]]}))
        exec(python_code)
        self.write(json.dumps({"result": vars()[result_name]}))
        log.info("executed")
