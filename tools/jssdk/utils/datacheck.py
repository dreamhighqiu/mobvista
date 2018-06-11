# -*- coding: utf-8 -*-
'''
Created on ：2018/6/4:14:07

@author: yunxia.qiu
'''
from hamcrest import *
# JSON数据递归检查
def check_json_data(expected_data, real_data, msg=""):
    # assert_that(real_data, not_none(), "%s real_data is none" % msg)
    # assert_that(expected_data, not_none(), "%s expected_data is none" % msg)

    if "*" == expected_data:
        assert_that(real_data, is_not(any_of(None, "")), msg)  # 全匹配只判定非空
    elif isinstance(expected_data,str) and expected_data.startswith("!"):
        assert_that(real_data[1:], is_not(expected_data), msg)
    elif isinstance(expected_data,str) and expected_data.endswith("*"):
        assert_that(real_data,starts_with(expected_data[:-1]), msg) #正则匹配
    elif isinstance(expected_data,str) and expected_data.startswith("^"):
        assert_that(real_data, starts_with(expected_data[1:]), msg) #正则匹配
    elif isinstance(expected_data,str) and expected_data.startswith("$"):
        assert_that(real_data, ends_with(expected_data[1:]), msg) #正则匹配

    elif isinstance(expected_data, dict):
        assert_that(real_data, instance_of(dict),
                    "%s real_data is not dict" % msg)
        # 注意expected_data与real_data是被包含关系也可通过
        for key in expected_data:
            if "not exists" == expected_data[key] or expected_data[key] is None:
                assert_that(real_data, is_not(has_key(key)),"%s real_data exists" % msg)
            else:
                assert_that(real_data, has_key(key))
                check_json_data(expected_data[key], real_data[
                            key], "key <%s>" % key)

    elif isinstance(expected_data, list):
        assert_that(real_data, instance_of(list),
                    "%s real_data is not list" % msg)
        assert_that(len(real_data), is_(len(expected_data)),
                    "%s real_data length is not expected" % msg)
        for _expected_data, _real_data in zip(expected_data, real_data):
            check_json_data(_expected_data, _real_data)

    else:
        assert_that(real_data, is_(expected_data), msg)
