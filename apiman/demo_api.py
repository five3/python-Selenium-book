#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, sys, getopt, json, os
import mimetypes, codecs, re
from pymongo import MongoClient
from hook import *
from Validator import Validator
import time

class utils(object):
    def __init__(self):
        pass

CONTEXT = {"continue" : True, "utils" : utils()}
COUNT = PASS = FAIL = SKIP = 0
QUITE = False
USAGE = 'Usage: \r\n\t' \
            '%s -u http://www.baidu.com -m get' % sys.argv[0]


def parse_args():
    global QUITE
    opts, args = getopt.getopt(sys.argv[1:], "qhc:d:e:f:m:t:u:v:C:D:E:H:N:P:")
    headers = {}
    files = []
    url = method = data = encoding = expect = \
        config_file = db_str = test_name = test_priority = \
        category = tag = version = None
    for op, value in opts:
        if op == "-u":
            url = value
        elif op == "-m":
            method = value
        elif op == '-d':
            try:
                data = json.loads(value)
            except Exception, ex:
                data = value
        elif op == '-H':
            try:
                headers.update(json.loads(value))
            except Exception, ex:
                print 'ERROR: headers format error'
                sys.exit(1)
        elif op == '-f':
            t = tuple(value.split(':'))
            files.append(t)
        elif op == '-e':
            encoding = value
        elif op == '-E':
            expect = value
        elif op == '-C':
            config_file = value
        elif op == '-D':
            db_str = value
            # config_file = 'testdata.json'
        elif op == '-N':
            test_name = value
        elif op == '-P':
            test_priority = value
        elif op == '-c':
            category = value
        elif op == '-t':
            tag = value
        elif op == '-v':
            version = value
        elif op == '-q':
            QUITE = True
        elif op == "-h":
            print USAGE
            sys.exit()
    return {
        'url' : url,
        'method' : method,
        'data' : data,
        'encoding' : encoding,
        'files' : files,
        'headers' : headers,
        'expect' : expect,
        'config_file' : config_file,
        'db_str' : db_str,
        'test_name' : test_name,
        'test_priority' : test_priority,
        'category' : category,
        'tag' : tag,
        'version' : version
    }


def warp_files(files):
    multiple_files = []
    for ft in files:
        if not isinstance(ft, tuple):
            raise TypeError, "文件子项不是元组类型"
        if len(ft) < 2 or len(ft) > 3:
            raise ValueError, "文件子项长度错误"

        field = ft[0]
        file_path = ft[1]
        file_name = os.path.basename(file_path)
        if len(ft) == 3:
            mime = ft[2]
        else:
            mime = mimetypes.guess_type(file_path)[0]

        t = (field, (file_name, open(file_path, 'rb'), mime))
        multiple_files.append(t)

    return multiple_files


def demo(url, method='get', data=None, headers=None, files=None, encoding='utf-8'):
    method = method.strip().lower() \
        if method and isinstance(method, str) else 'get'
    if hasattr(requests, method):
        func = getattr(requests, method)
        if method in ['post', 'put', 'patch']:
            multiple_files = []
            if files:
                multiple_files = warp_files(files)
            rsp = func(url, data, headers=headers, files=multiple_files)
        else:
            rsp = func(url, params=data, headers=headers)
    else:
        rsp = requests.get(url, params=data, headers=headers)
    rsp.encoding = encoding
    code = rsp.status_code
    txt = rsp.text
    return code, txt


def verify_result(code, txt, expect, ttype):
    if code != 200:
        msg = u'测试失败：响应代码期望值为200，实际为', code
        print msg
        return False, msg
    r, msg = Validator.verify(txt, expect, ttype)
    if r:
        print u'测试通过'
        return True, None
    else:
        return False, msg


def run(args):
    global CONTEXT, PASS, FAIL, SKIP
    if 'url' not in args or 'method' not in args:
        SKIP += 1
    print u'开始执行测试用例: %s' % args.get('name', u'未命名')
    request_data = [args['url'], args['method'],
                     args.get('data'), args.get('headers'),
                     args.get('files'), args.get('encoding')]
    [fun(request_data, CONTEXT) for fun in PRE_REQUEST_LIST]
    code, txt = demo(*request_data)
    [fun(code, txt, CONTEXT) for fun in POST_REQUEST_LIST]
    args['resp_code'] = code
    args['resp_text'] = txt
    if not QUITE:
        print code
        print txt
    flag, msg = verify_result(code, txt, args.get('expect', ''), args.get('checkType', "include"))
    args['result'] = flag
    args['msg'] = msg
    add_result(args)
    add_log(args)
    [fun(flag, CONTEXT) for fun in POST_TESTING_LIST]
    if flag:
        PASS += 1
    else:
        FAIL += 1
    print u'测试用例执行结束: %s' % args['name']
    return flag


def add_result(test_data):
    result_info = {
        "task_name" : test_data.get('task_name'),
        "project_name" : test_data.get('project_name'),
        "testcase_name" : test_data.get('name'),
        "category" : test_data.get('category'),
        "version" : test_data.get('version'),
        "result" : test_data.get('result'),
        "time" : int(time.time())
    }
    write_mongo(record=result_info)


def add_summary(task_name, summary):
    info = {"task_name" : task_name}
    write_mongo(collection="summary", record=info.update(summary))


def add_log(test_data):
    test_log = {
        "task_name": test_data.get('task_name'),
        "project_name": test_data.get('project_name'),
        "testcase_name": test_data.get('name'),
        "resp_code": test_data.get('resp_code'),
        "resp_text": test_data.get('resp_text'),
        "expect": test_data.get('expect'),
        "checkType": test_data.get('checkType'),
        "msg": test_data.get('msg')
    }
    write_mongo(collection="testlog", record=test_log)


def write_mongo(host="127.0.0.1", port=27017, db_name='apiman', collection='testresult', record={}):
    client = MongoClient(host, port)
    db = client[db_name]
    coll = db[collection]
    return coll.insert_one(record) ##添加记录


def read_config(fp, encoding="utf-8"):
    with codecs.open(fp, "rb", encoding) as f:
        txt = f.read()
        return json.loads(txt)


def read_mongo(host="127.0.0.1", port=27017, db_name='apiman', collection='testdata', condition={}):
    client = MongoClient(host, port)
    db = client[db_name]
    coll = db[collection]
    return coll.find(condition) ##获取记录


def run_with_json(config_file):
    global CONTEXT, COUNT
    if os.path.exists(config_file):
        test_data = read_config(config_file)
        [fun(test_data, CONTEXT) for fun in PRE_ALL_TESTING_LIST]
        index = 0
        COUNT = len(test_data)
        for data in test_data:
            index += 1
            run_with_data(data, index, 'json')
    else:
        print 'CONFIG File Not Exist'
        exit(1)


def run_with_db(args):
    global CONTEXT, COUNT
    db_str = args['db_str']
    test_name = args['test_name']
    test_priority = args['test_priority']
    category = args['category']
    tag = args['tag']
    version = args['version']
    task_name = args['task_name']
    if not task_name:
        task_name = int(time.time()) ##默认执行任务名
    if db_str.strip() == '*':
        test_data = read_mongo()
    else:
        db_info = db_str.split(':')
        condition = {}
        if test_name:
            partten = re.compile(test_name, re.I)
            condition['name'] = partten
        if test_priority:
            if not test_priority.isdigit():
                print 'Priority Must Be a Num'
                exit(3)
            condition['priority'] = int(test_priority)
        if category:
            condition['category'] = category
        if tag:
            condition['tags'] = {"$elemMatch": {tag: 1}}
        if version:
            condition['version'] = version
        if condition:
            db_info.append(condition)
        try:
            test_data = read_mongo(*db_info)
        except:
            print 'DB Connect Failure'
            exit(2)
    [fun(test_data, CONTEXT) for fun in PRE_ALL_TESTING_LIST]
    index = 0
    COUNT = len(test_data)
    for data in test_data:
        index += 1
        data['task_name'] = task_name
        run_with_data(data, index, 'db')


def run_with_data(data, index, ttype='db'):
    [fun(data, index, CONTEXT) for fun in PRE_TESTING_LIST]
    if not CONTEXT['continue']:
        return
    data = merge_template(data, ttype)
    return run(data)
CONTEXT['utils'].run_with_data = run_with_data


def get_json_template(name):
    templates = read_config('template.json')
    if name in templates:
        return templates[name]


def get_db_template(name):
    templates = read_mongo(collection='template',
                           condition={'name' : name})
    if templates and len(templates) > 0:
        return templates[0]


def merge_template(data, ttype):
    temp = data.get('template')
    if temp and temp.strip():
        if ttype == 'json':
            template = get_json_template(temp.strip())
        elif ttype == 'db':
            template = get_db_template(temp.strip())
        if template:
            template.update(data)
            data = template
    return data


def get_test_data_by_case_name(name):
    condition = {"name" : name}
    test_data = read_mongo(condition=condition)
    return test_data[0] if test_data else None
CONTEXT['utils'].get_test_data_by_case_name=get_test_data_by_case_name


def main(args):
    global COUNT
    task_name = args.get('task_name', '')
    task_name = '%s_%s' % (task_name, int(time.time()))
    args['task_name'] = task_name
    config_file = args.get('config_file')
    db_str = args.get('db_str')
    if config_file:
        run_with_json(config_file)
    elif db_str:
        run_with_db(args)
    elif args['url'] and args['method']:
        [fun(args, 1, CONTEXT) for fun in PRE_TESTING_LIST]
        COUNT = 1
        run(args)
    else:
        print USAGE

    summary = {
        'count' : COUNT,
        'pass' : PASS,
        'fail' : FAIL,
        'skip' : SKIP
    }
    add_summary(task_name, summary)
    [fun(summary, CONTEXT) for fun in POST_ALL_TESTING_LIST]
    return summary

if __name__ == '__main__':
    args = parse_args()
    main(args)
