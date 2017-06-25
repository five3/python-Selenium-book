#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
from selenium.common.exceptions import NoSuchElementException
from Result.Result import Result
from Result.DBResult import DBResult
result = Result()
dbResult = DBResult()
def element_not_found_exception(func):
    def not_found(self, locator):
        try:
            return func(self, locator)
        except NoSuchElementException:
            msg = 'element not found for locator:'+locator+'At method:'+func.__name__
            dbResult.log_error(self, msg)
            result.log_error(msg)
            return None
    return not_found

def assert_logger(func):
    def assertlogger(self):
        try:
            msg = 'Test Case is:'+func.__name__
            dbResult.log_info(self, msg)
            result.log_info(msg)
            return func(self)
        except AssertionError, ex:
            msg = 'AssertError in: %s.%s' % (self.__class__.__name__, func.__name__)
            dbResult.log_error(self, msg)
            dbResult.log_fail(self)
            result.log_error(msg)
            result.log_fail()
    assertlogger.__name__=func.__name__
    return assertlogger

def exception_logger(func):
    def exceptionlogger(self):
        try:
            return func(self)
        except Exception, ex:
            # print sys.exc_info()
            if True: ##debug is Ttrue?
                print traceback.print_exc()  ##打印完整堆栈用于定位代码行
            msg = "%s:%s At method:%s" % (Exception, ex, func.__name__)
            result.log_error(msg)
            dbResult.log_error(self, msg)
    return exceptionlogger

def name_logger(func):
    def namelogger(self):
        self.__class__.test_result_id = dbResult.log_init('', self.__class__.__name__, func.__name__) ##设置test_result_id
        result.log_info('Test Class is:'+self.__class__.__name__)
        return func(self)
    namelogger.__name__=func.__name__
    return namelogger

class NOTESTDATAERROR(Exception):
    def __init__(self, module, test_case):
        self.value = '%s: Module: %s, TestCase: %s' % (self.__class__.__name__, module, test_case)
    def __str__(self):
        return repr(self.value)

class NOLOCATORERROR(Exception):
    def __init__(self, module, test_case, name):
        self.value = '%s: Module: %s, TestCase: %s' % (self.__class__.__name__, module, test_case)
    def __str__(self):
        return repr(self.value)
