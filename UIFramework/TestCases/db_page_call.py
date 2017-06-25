#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from Errors.ExceptionWarpper import *
from Data.DataPool import DBDataPool
from Pages.BaiduHome import BaiduHome
from Result.DBResult import DBResult
class TestDemo(unittest.TestCase):
    @exception_logger
    @name_logger
    def setUp(self):
        self.wd = webdriver.Chrome()
        self.dp = DBDataPool(self.__class__.__name__)
        self.wd.get(self.dp.get('BAIDU_HOME_URL'))
        self.page = BaiduHome(self.wd)
        self.result = DBResult()

    @exception_logger
    @assert_logger
    def test_sample(self):
        self.page.key_worlds_input(self.dp.get('SELENIUM'))
        self.page.search_click()
        self.result.log_info(self,'The search button is clicked')
        assert True
        self.result.log_pass(self)

    @exception_logger
    def tearDown(self):
        self.wd.close()

if __name__=='__main__':
    unittest.main()