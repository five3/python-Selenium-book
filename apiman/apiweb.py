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
        result = {'error_code' : -1, 'error_msg' : '请求数据错误!'}
    return json.dumps(result)

@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

