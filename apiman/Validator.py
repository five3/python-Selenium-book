#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, json
from jsonpath import jsonpath


class Validator(object):
    @staticmethod
    def _get_method_mapping():
        return {
            "equal" : Validator._equal,
            "include" : Validator._include,
            "regex" : Validator._regex,
            "json" : Validator._json
        }

    @staticmethod
    def verify(content, expect, vtype):
        content = content.strip()
        expect = expect.strip()
        func = Validator._get_method_mapping().get(vtype)
        if func and callable(func):
            return func(content, expect)

    @staticmethod
    def _equal(content, expect):
        msg = u'期望结果为：%s， 实际结果为：%s' % (expect, content)
        return True if content == expect else (False, msg)

    @staticmethod
    def _include(content, expect):
        msg = u'期望结果为包含：%s，实际未包含' % expect
        return True if expect in content else (False, msg)

    @staticmethod
    def _regex(content, expect):
        r = re.search(expect, content, re.DOTALL)
        msg = u"期望结果为匹配：%s，实际未匹配成功" % expect
        return True if r else (False, msg)

    @staticmethod
    def _json(content, expect):
        if '|' in expect:
            jpath, value = expect.split('|', 1)
        else:
            jpath, value = expect, None

        try:
            nodes = jsonpath(json.loads(content), jpath)
        except:
            msg = u"响应内容不是JSON格式"
            return False, msg

        if nodes:
            if value and nodes[0] != value:
                msg = u'期望[%s]节点结果为：%s， 实际结果为：%s' % (jpath, value, nodes[0])
                return False, msg
        else:
            msg = u'期望结果为存在节点：%s， 实际未找到该节点' % jpath
            return False, msg
        return True, None

if __name__=='__main__':
    flag, msg = Validator.verify('{"success" : "true"}', "$.success|false", "json")
    print flag
    print msg
