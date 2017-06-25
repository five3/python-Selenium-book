#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from Errors.ExceptionWarpper import NOTESTDATAERROR

class DBDataPool(object):
    def __init__(self, test_case, module=None):
        self.test_case = test_case
        self.module = module

    def get(self, name, defalut=None):
        where = ' AND 1=1 '
        if self.module:
            where += ''' AND module='%s' ''' % self.module
        sql = '''SELECT value FROM test_data
                WHERE test_case='%s'
                AND name='%s'
                AND status='active' %s;''' % (self.test_case, name, where)
        data = self.select_data(sql)
        if data:
            return data[0]
        elif defalut is not None:
            return defalut
        else:
            raise NOTESTDATAERROR(self.module, self.test_case, name)

    def select_data(self, sql):
        db = MySQLdb.connect("localhost","root","root","datapool" )  ##数据库连接
        cursor = db.cursor()  ##获取游标
        cursor.execute(sql)  ##执行sql语句
        data = cursor.fetchone()  ##获取一条查询结果数据
        db.close()
        return data

FileDataPool = {
    'BAIDU_HOME_URL' : 'http://www.baidu.com',
    'SELENIUM' : 'selenium',

    'LOGIN_DEMO_URL' : 'http://www.testdoc.org',
    'USER_NAME' : 'test',
    'PASSWORD' : 'test',
}