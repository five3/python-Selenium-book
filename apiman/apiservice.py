#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, traceback, sys
from demo_api import main, get_task_list, get_condition_by_test_set, save_test_set, get_result_list

def do_testing_with_db(args):
    try:
        return main(args)
    except Exception, ex:
        print ex.message
        return {'error_code' : -2, 'error_msg' : '执行批量测试任务异常!'}


def do_testing_with_data(args):
    # try:
    if args.get('files'):
        f_list = args.get('files').split(',')
        args['files'] = [tuple(f.split(':')) for f in f_list]
    if args.get('data'):
        try:
            args['data'] = json.loads(args.get('data'))
        except:
            pass
    if args.get('headers'):
        try:
            args['headers'] = json.loads(args.get('headers'))
        except Exception, ex:
            print ex.message
            return {'error_code' : -3, 'error_msg' : '解析请求头异常!'}
    return main(args)
    # except Exception, ex:
    #     print ex.message
    #     return {'error_code' : -4, 'error_msg' : '执行单次测试任务异常!'}

def to_dict(form):
    d = {}
    for k in form.keys():
        d[k] = form.get(k)
    return d