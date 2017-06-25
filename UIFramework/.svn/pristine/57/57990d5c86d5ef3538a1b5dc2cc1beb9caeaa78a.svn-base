#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PageBase import PageBase
from Locator.Locator import DBLocator

class BaiduHome(PageBase):
    def __init__(self, wd):
        locator = DBLocator(self.__class__.__name__)
        PageBase.__init__(self, wd, locator)

    def __del__(self):
        pass

    def key_worlds_input(self, value):
        self.get_element('KEY_WORLDS').send_keys(value)

    def search_click(self):
        self.get_element('SEARCH').click()


