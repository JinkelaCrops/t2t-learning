"""
为了能够按行读取，选定区间读取，以及并发写入，需要以下的修改
1. RemoteIO.save 写入方式可选
2. RemoteIO.laod 读取起始行及行数可选

file-down的目标文件夹可选
"""

import requests
import json


class RemoteIO(object):
    def __init__(self, host):
        self.host = host

    def save(self, data: list, file_name: str, write_mode: str):
        payload = {
            "data": json.dumps(data),
            "file_name": file_name,
            "write_mode": write_mode
        }
        requests.post(url="http://%s:8000/wt" % self.host, data=payload)

    def load(self, file_name: str, read_start: int, read_end: int):
        payload = {
            "file_name": file_name,
            "read_start": read_start,
            "read_end": read_end
        }
        res = requests.post(url="http://%s:8000/sd" % self.host, data=payload)
        return res.json()["result"]

    def exec(self, python_code: str, result_name: str):
        payload = {
            "python_code": python_code,
            "result_name": result_name
        }
        res = requests.post(url="http://%s:8000/ex" % self.host, data=payload)
        return res.json()["result"]

    def rm(self, directory_list: list):
        payload = {
            "directory_list": json.dumps(directory_list),
        }
        requests.post(url="http://%s:8000/rm" % self.host, data=payload)

    def mk(self, directory_list: list):
        payload = {
            "directory_list": json.dumps(directory_list),
        }
        requests.post(url="http://%s:8000/mk" % self.host, data=payload)

    def ls(self, directory_list: list, recursive: bool, showdir: bool):
        payload = {
            "directory_list": json.dumps(directory_list),
            "recursive": recursive,
            "showdir": showdir,
        }
        res = requests.post(url="http://%s:8000/ls" % self.host, data=payload)
        return res.json()["result"]

    def fp(self, file_list: list, bucket_size: int):
        payload = {
            "file_list": json.dumps(file_list),
            "bucket_size": bucket_size,
        }
        res = requests.post(url="http://%s:8000/fp" % self.host, data=payload)
        return res.json()["result"]

    def trans(self, args):
        payload = {
            "args": json.dumps(args)
        }
        res = requests.post(url="http://%s:8000/trans" % self.host, data=payload)
        return res.json()["result"]
