#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Pages import LoginPage


class LoginModel(object):
    def __init__(self, wd):
        self.page = LoginPage(wd)

    def __del__(self):
        pass

    def login(self,username, password):
        self.page.user_name_input(username)
        self.page.passwrod_input(password)
        self.login_click()




