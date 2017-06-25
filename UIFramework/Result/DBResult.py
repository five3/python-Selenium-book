#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys,os
import MySQLdb
def findcaller(func):
    def wrapper(*args):
        f=sys._getframe()
        d = {
            'file_name' : os.path.basename(f.f_back.f_code.co_filename),
            'func_name' : f.f_back.f_code.co_name,
            'line_no' : f.f_back.f_lineno
        }
        args = list(args)
        args.append(d)
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
class DBResult(object):
    def __init__(self):
        self.__connect()
        self.__class__.test_result_id = 1

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def __connect(self):
        self.db = MySQLdb.connect("localhost","root","root","datapool" )  ##数据库连接
        self.cursor = self.db.cursor()  ##获取游标

    def log_init(self, test_set, test_case, test_method):
        sql = '''INSERT INTO result (test_set, test_case, test_method, result, createAt)
            VALUES ('%s','%s','%s','%s',now())''' % (test_set, test_case, test_method, 'FAIL')
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.lastrowid

    def log_pass(self, case):
        return self.__log_result(case, 'PASS')

    def log_fail(self, case):
        return self.__log_result(case, 'FAIL')

    def __log_result(self, case, result):
        sql = '''UPDATE result SET result='%s'
                WHERE id=%s''' % (result, case.__class__.test_result_id)
        r = self.cursor.execute(sql)
        self.db.commit()
        return r

    @findcaller
    def log_debug(self, case, msg, caller={}):
        return self.__log_info(case, msg, 'DEBUG', caller)

    @findcaller
    def log_info(self, case, msg, caller={}):
        return self.__log_info(case, msg, 'INFO', caller)

    @findcaller
    def log_warning(self, case, msg, caller={}):
        return self.__log_info(case, msg, 'WARNING', caller)

    @findcaller
    def log_error(self, case, msg, caller={}):
        return self.__log_info(case, msg, 'ERROR', caller)

    @findcaller
    def log_critical(self, case, msg, caller={}):
        return self.__log_info(case, msg, 'CRITICAL', caller)

    def __log_info(self, case, msg, level, caller={}):
        sql = '''INSERT INTO log (`result_id`,`file_name`,`func_name`,`line_no`,`level`,`log`, createAt)
            VALUES ('%s','%s','%s','%s','%s','%s', now())''' % (case.__class__.test_result_id, caller.get('file_name'),
                                                         caller.get('func_name'), caller.get('line_no'), level, msg)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.lastrowid

if __name__=='__main__':
    result = DBResult()
    result.logInit('testSet', 'BaiduHome', 'test_demo')
    result.logDebug(result, 'The debug message')
    result.logInfo(result, 'The info message')
    result.logPass(result)



