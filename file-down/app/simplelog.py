# coding=utf-8
import logging


# 简易日志脚本
class Logger():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def __init__(self,loggername,logpath=None):
        self.loggername = loggername
        self.logpath = logpath
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)

    def add_fh(self):
        if self.logpath == None:
            raise 'logpath is None'
        else:
            fh = logging.FileHandler(self.logpath)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)

    def add_ch(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def log(self,log_type=None):
        if log_type == 'F':
            self.add_fh()
        elif log_type == 'C':
            self.add_ch()
        else:
            self.add_ch()
            self.add_fh()
        return self.logger

# other class
class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        pass 


