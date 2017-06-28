#!/usr/bin/env python
# -*- coding: utf-8 -*-

PRE_ALL_TESTING_LIST = []
PRE_TESTING_LIST = []
PRE_REQUEST_LIST = []
POST_REQUEST_LIST = []
POST_TESTING_LIST = []
POST_ALL_TESTING_LIST = []


def pre_all_testing_demo(all_test_data, context):
    '''
    all_test_data: 所有的测试数据, list
    context: 测试用例上下文信息, dict
    return: None, 所有信息通过上下文来传递
    '''
    pass
PRE_ALL_TESTING_LIST.append(pre_all_testing_demo)


def pre_testing_demo(test_data, index, context):
    '''
    test_data: 当前用例的测试数据, dict
    index: 当前用例的执行轮次, int
    context: 测试用例上下文信息, dict
    return: None, 所有信息通过上下文来传递
    '''
    pass
PRE_TESTING_LIST.append(pre_testing_demo)


def pre_case(test_data, index, context):
    if not context['continue']:
        return
    if 'pre_case' in test_data:
        case_name = test_data['pre_case']
        pre_test_data = context['utils'].get_test_data_by_case_name(case_name)
        if pre_test_data:
            r = context['utils'].run_with_data(pre_test_data, index)
            context['continue'] = r
PRE_TESTING_LIST.append(pre_case)


def pre_request_demo(request_data, context):
    '''
    request_data: 当前请求的测试数据, dict
    context: 测试用例上下文信息, dict
    return: None, 所有信息通过上下文来传递
    '''
    pass
PRE_REQUEST_LIST.append(pre_request_demo)


def post_request_demo(response_code, response_data, context):
    '''
    response_code: 当前请求的响应代码, int
    response_data: 当前请求的响应数据, string
    context: 测试用例上下文信息, dict
    return: None, 所有信息通过上下文来传递
    '''
    pass
POST_REQUEST_LIST.append(post_request_demo)


def post_testing_demo(result, test_data, context):
    '''
    result: 当前用例的执行结果，boolean
    test_data: 当前用例的测试数据, dict
    context: 测试用例上下文信息, dict
    return: None, 所有信息通过上下文来传递
    '''
    pass
POST_TESTING_LIST.append(post_testing_demo)

def post_case(result, test_data, context):
    pass

def post_all_testing_demo(summary, context):
    '''
    summary: 所有测试结果统计信息，dict
    context: 测试用例上下文信息, dict
    return: None, 所有信息通过上下文来传递
    '''
    pass
POST_ALL_TESTING_LIST.append(post_all_testing_demo)