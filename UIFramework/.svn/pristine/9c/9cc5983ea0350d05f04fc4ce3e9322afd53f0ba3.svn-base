#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Pages import PageBase
from Locator.Locator import DBLocator

class DashBoard(PageBase):
    def __init__(self, wd):
        PageBase.__init__(self, wd, DBLocator)

    def __del__(self):
        pass

    def get_user_name(self):
        self.get_element('USER_DISPALY_NAME').get_attribute('innerText')






