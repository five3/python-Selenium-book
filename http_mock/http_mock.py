#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Flask, request
app = Flask(__name__)

MOCK_MAPPING = {
    "date/year": {
        "GET" : {
            "headers":{
                "user-agent": ""
            },
            "data":{
                "current": True
            },
            "response": {"year": "2017"},
            "default": "No Mock Header Matched"
        },
        "POST" : {
            "headers":{
            },
            "data":{
            },
            "response": {"year": "2017"},
            "default": "No Mock Header Matched"
        },
        "default": "Method Not Support"
    },
    "default": "URL Not Found"
}

@app.route('/')
def index():
    return 'Welcome to HTTP Mocker!'

@app.route('/<path:url>', methods= ['GET', 'POST'])
def dispatch(url):
    req_headers = request.headers
    url = url.rstrip('/')
    if url in MOCK_MAPPING:
        method_mapping = MOCK_MAPPING[url]
        if request.method in method_mapping:
            resp_mapping = method_mapping[request.method]
            if 'headers' in resp_mapping and resp_mapping['headers']:
                headers = resp_mapping['headers']
                for k, v in headers.items():
                    if k in req_headers:
                        if v and v.strip():
                            req_v = req_headers[k].strip().lower()
                            if req_v != v.strip().lower():
                                return resp_mapping['default']
                    else:
                        return resp_mapping['default']
            if 'data' in resp_mapping and resp_mapping['data']:
                data = resp_mapping['data']
                if request.method == 'POST':
                    content_type = req_headers.get['Content-Type']
                    if content_type.startswith('application/x-www-form-urlencoded'):
                        req_data = request.form
                    elif content_type.startswith('multipart/form-data'):
                        req_data = request.form
                        req_file = request.files
                    else:
                        req_data = request.data
                        if data.strip() != req_data:
                            return resp_mapping['default']
                else:
                    req_data = request.args
                for k, v in data.items():
                    if k in req_data:
                        if v and v.strip():
                            req_v = req_data[k].strip().lower()
                            if req_v != v.strip().lower():
                                return resp_mapping['default']
                    elif k in req_file:
                        file_obj = req_file[k]
                        if v.strip() != file_obj.filename:
                            return resp_mapping['default']
                    else:
                        return resp_mapping['default']
            return json.dumps(resp_mapping['response'])
        else:
            return method_mapping['default']
    else:
        return MOCK_MAPPING['default']

if __name__ == '__main__':
    app.run(debug=True)