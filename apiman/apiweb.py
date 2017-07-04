#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo
from flask import request
from apiservice import *
import json

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'apiman'
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testing', methods=['POST'])
def testing():
    data = to_dict(request.form)
    print data
    if data.get('db_str'):
        db_str = data.get('db_str')
        if db_str:
            result = do_testing_with_db(data)
    elif data.get('url') and data.get('method'):
        url = data.get('url')
        method = data.get('method')
        if url and method:
            result = do_testing_with_data(data)
    else:
        result = {'error_code' : -1, 'error_msg' : u'请求数据错误!'}
    return json.dumps(result)

@app.route('/task')
def status():
    tasks = get_task_list()
    return render_template('task.html', tasks=tasks)

@app.route('/result')
def result():
    results = get_task_list()
    return render_template('result.html', results=results)

@app.route('/testset', methods=['POST', 'GET'])
def test_set():
    if request.method=='GET':
        return render_template('testset.html')
    elif request.method=='POST':
        data = request.form
        result = save_test_set(data)
        if result:
            return json.dumps({"msg": u"保存用例集成功"})


@app.route('/api_testing', methods=['POST', 'GET'])
def api_testing():
    if request.method=='POST':
        test_set = request.form.get('test_set')
    else:
        test_set = request.args.get('test_set')
    condition = get_condition_by_test_set(test_set)
    if condition:
        result = do_testing_with_db(condition)
    else:
        result = {'error_code': -5, 'error_msg': u'获取测试数据失败!'}
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

