#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import logging.config
import sys,os
def findcaller(func):
    def wrapper(*args):
        f=sys._getframe()
        filename=f.f_back.f_code.co_filename
        funcname=f.f_back.f_code.co_name
        lineno=f.f_back.f_lineno
        args = list(args)
        args.append('%s.%s.%s' % (os.path.basename(filename), funcname, lineno))
        func(*args)
    return wrapper

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Result(object):
    def __init__(self):
        cur = os.path.split(os.path.realpath(__file__))[0]
        logging.config.fileConfig(os.path.join(cur,"logger.conf"))
        self.__resulter = logging.getLogger("result")
        self.__infor = logging.getLogger("infomation")

    @findcaller
    def log_pass(self, caller=''):
        self.__resulter.critical('PASS::'+caller)

    @findcaller
    def log_fail(self, caller=''):
        self.__resulter.critical('FAIL::'+caller)

    @findcaller
    def log_debug(self, msg, caller=''):
        self.__infor.debug('[%s] %s' % (caller, msg))

    @findcaller
    def log_info(self, msg, caller=''):
        self.__infor.info('[%s] %s' % (caller, msg))

    @findcaller
    def log_warning(self, msg, caller=''):
        self.__infor.warning('[%s] %s' % (caller, msg))

    @findcaller
    def log_error(self, msg, caller=''):
        self.__infor.error('[%s] %s' % (caller, msg))

    @findcaller
    def log_critical(self, msg, caller=''):
        self.__infor.critical('[%s] %s' % (caller, msg))

if __name__=='__main__':
    result = Result()
    result.logPass()
    result.logFail()
    result.logDebug('The debug message')
    result.logInfo('The info message')




