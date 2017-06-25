#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Pages import PageBase
from Locator.Locator import DBLocator

class LoginPage(PageBase):
    def __init__(self, wd):
        PageBase.__init__(self, wd, DBLocator)

    def __del__(self):
        pass

    def user_name_input(self, value):
        self.get_element('USER_NAME').send_keys(value)

    def passwrod_input(self, value):
        self.get_element('PASSWORD').send_keys(value)

    def login_click(self):
        self.get_element('LOGIN').click()





