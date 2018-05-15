# -*-coding: utf-8 -*-
# __author__ : tinytiger
# __time__   : '2018/1/4 11:08'

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.
import tornado.web
import json
import os
import shutil

from app.biz import understand_data
from app.biz import bucket_to_pointer
from app.biz import file_scan
from app.biz import Sync_io
from tornado.escape import _unicode
from tornado.web import HTTPError

# from loginst import logger
from app.simplelog import Logger

logger = Logger("file-down", "file-down.log").log("F")
sync_io = Sync_io()


class WriteDownHandler(tornado.web.RequestHandler):
    def decode_argument(self, value, name=None):
        try:
            return _unicode(value)
        except UnicodeDecodeError:
            return bytes(value)
        except:
            raise HTTPError(400, "[WriteDownHandler]: Invalid unicode or bytes in %s: %r" %
                            (name or "url", value[:40]))

    def post(self):
        logger.info("[WriteDownHandler]: get data from memory")
        write_data = self.get_argument("data")
        write_data = understand_data(write_data)
        path = self.get_argument("file_name")
        if not isinstance(path, str):
            logger.warn("[WriteDownHandler]: TypeError: not a file name")
            return
        write_flag = self.get_argument("write_mode")
        if not isinstance(write_flag, str):
            logger.warn("[WriteDownHandler]: TypeError: write_flag is not string")
            return
        logger.info("[WriteDownHandler]: write data into %s" % path)
        sync_io.write(path, {"flag": write_flag, "data": write_data})
        logger.info("[SendOutHandler]: write done")


class SendOutHandler(tornado.web.RequestHandler):
    def post(self):
        path = self.get_argument("file_name")
        if not isinstance(path, str):
            logger.warn("[SendOutEndHandler]: TypeError: file_name is not string")
            return
        read_start = int(self.get_argument("read_start"))
        read_end = int(self.get_argument("read_end"))
        logger.info("[SendOutHandler]: send data from %s [%s] -> [%s]" % (path, read_start, read_end))
        self.write(sync_io.read(path, {"start": read_start, "end": read_end}))
        logger.info("[SendOutHandler]: send done")


class ExecHandler(tornado.web.RequestHandler):
    def post(self):
        python_code = self.get_argument("python_code")
        result_name = self.get_argument("result_name")
        if not isinstance(python_code, str):
            logger.warn("[ExecHandler]: TypeError: python_code is not string")
            return
        if not isinstance(result_name, str):
            logger.warn("[ExecHandler]: TypeError: result_name is not string")
            return
        logger.info("[ExecHandler]: execute python code: %s" % python_code)
        exec(python_code)
        self.write(json.dumps({"result": vars()[result_name]}))


class RemoveHandler(tornado.web.RequestHandler):
    def post(self):
        dir_list = self.get_argument("directory_list")
        dir_list = understand_data(dir_list)
        if not isinstance(dir_list, list) and not all(map(lambda x: isinstance(x, str), dir_list)):
            logger.warn("[RemoveHandler]: TypeError: not directory list")
            return
        for dir_path in dir_list:
            logger.info("[RemoveHandler]: remove %s" % dir_path)
            shutil.rmtree(dir_path)


class MakeDirHandler(tornado.web.RequestHandler):
    def post(self):
        dir_list = self.get_argument("directory_list")
        dir_list = understand_data(dir_list)
        if not isinstance(dir_list, list) and not all(map(lambda x: isinstance(x, str), dir_list)):
            logger.warn("[MakeDirHandler]: TypeError: not directory list")
            return
        for dir_path in dir_list:
            if not os.path.exists(dir_path):
                logger.info("[MakeDirHandler]: make %s" % dir_path)
                os.makedirs(dir_path)


class ListHandler(tornado.web.RequestHandler):
    def post(self):
        dir_list = self.get_argument("directory_list")
        dir_list = understand_data(dir_list)
        recursive = self.get_argument("recursive")
        showdir = self.get_argument("showdir")
        if not isinstance(dir_list, list) and not all(map(lambda x: isinstance(x, str), dir_list)):
            logger.warn("[ListHandler]: TypeError: not directory list")
            return
        all_file_list = []
        for dir_path in dir_list:
            if os.path.exists(dir_path):
                logger.info("[ListHandler]: scaning %s" % dir_path)
                all_file_list += file_scan(dir_path, recursive, showdir)
        self.write(json.dumps({"result": all_file_list}))


class FilePointerGenHandler(tornado.web.RequestHandler):
    def post(self):
        file_list = self.get_argument("file_list")
        file_list = understand_data(file_list)
        bucket_size = int(self.get_argument("bucket_size"))
        if not isinstance(file_list, list) and not all(map(os.path.exists, file_list)):
            logger.warn("[FilePointerGenHandler]: TypeError: not file list or file not exist")
            return
        if bucket_size < 1:
            logger.warn("[FilePointerGenHandler]: TypeError: bucket size is smaller than 1")
            return
        file_pointer_dict = {}
        for file_path in file_list:
            logger.info("[FilePointerGenHandler]: splitting %s" % file_path)
            file_pointer_dict[file_path] = bucket_to_pointer(file_path, bucket_size)
        self.write(json.dumps({"result": file_pointer_dict}))
