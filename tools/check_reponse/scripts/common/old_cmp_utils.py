# encoding:utf-8

from scripts.common.file_utils import *
import json


def cmp_scv(src_csv, des_csv):
    pass


def cmp_dict_data_pass_diff(expect_dict, fact_dict, key_prefix="", set_pass=set(), set_diff=set(),
                            set_more=set(), set_less=set()):
    if expect_dict == fact_dict:
        return set_diff
    set_expect_keys = set(expect_dict.keys())
    set_fact_keys = set(fact_dict.keys())
    set_cmp = set_expect_keys.union(set_fact_keys)
    for key in set_cmp:
        cmp_key = str(key)
        if key_prefix:
            cmp_key = '{0}{1}'.format(key_prefix, key)
        if cmp_key in set_pass:
            continue
        expect_v = expect_dict.get(key)
        fact_v = fact_dict.get(key)
        if key in set_expect_keys.difference(set_fact_keys):
            set_less.add(cmp_key)
            write_log('{0} is less, expect value is {1} {2}'.format(cmp_key,type(expect_v), expect_v))
            continue
        if key in set_fact_keys.difference(set_expect_keys):
            set_more.add(cmp_key)
            write_log('{0} is more, fact value is {1} {2}'.format(cmp_key, type(fact_v), fact_v))
            continue
        if expect_v != fact_v:
            if not isinstance(fact_v, type(expect_v)):
                set_diff.add(cmp_key)
                write_log('{4} type is diff, \n\texpect: {0}\t{1}\n\tfact:{2}\t{3}'
                          .format(type(expect_v), expect_v, type(fact_v), fact_v, cmp_key))
                continue
            if isinstance(expect_v, dict):
                cmp_dict_data_pass_diff(expect_v, fact_v, cmp_key + '.', set_pass, set_diff, set_more, set_less)
            else:
                set_diff.add(cmp_key)
                try:
                    write_log('{0}:\n\texpect is : {1} {2}\n\tfact   is : {3} {4}'
                              .format(cmp_key, type(expect_v), expect_v, type(fact_v), fact_v))
                except Exception as e:
                    write_log('{0}:\n\texpect is : {1}\n\tfact   is : {2}'
                              .format(cmp_key, type(expect_v), type(fact_v)))
                    write_log(e, 'error')

    return set_diff, set_more, set_less


def cmp_dict_type(dict_expect, dict_fact, list_pass=None):
    if not list_pass:
        list_pass = []
    result = True
    list_diff = []
    set_keys = set(dict_expect.keys()).intersection(set(dict_fact.keys()))
    for key in set_keys:
        expect_type = type(dict_expect.get(key))
        fact_type = type(dict_fact.get(key))
        if expect_type != fact_type and key not in list_pass:
            # if expect_type in (int,long,float) and fact_type in(unicode,str):
            result = False
            msg = 'key: %s\n\t expect_type: %s\n\t fact_type: %s\n' % (key, expect_type, fact_type)
            list_diff.append(msg)
            write_log(msg)
    return result, list_diff


def find_all_tag_value(data, list_result, condition=None):
    if not isinstance(data, (list, dict)):
        return list_result
    data = data
    if isinstance(data, dict):
        data = data.values()
    for i in data:
        if isinstance(i, (list, dict)):
            find_all_tag_value(i, list_result, condition)
        else:
            if not condition or (condition and eval('i'+condition)):
                list_result.append(i)
    return list_result


def remove_str_digit(str_x):
    for x in str_x:
        if x.isdigit():
            str_x = str_x.replace(x, '')
    str_x = str_x.replace('..', '.*.')
    return str_x

def soup_dict(data_dict):
        """
        格式化dict
        :param data_dict:
        :return:
        """
        print(json.dumps(data_dict, indent=4, sort_keys=False, ensure_ascii=False))


def cmp_list(list_expect, list_fact, sort_key=None, ignore_order=True):
    if list_expect == list_fact:
        return True
    if not ignore_order:
        msg = 'is diff! \n' \
                    '\texpect is : {1} {2}\n' \
                    '\tfact   is : {3} {4}'.format(type(list_expect), list_expect, type(list_fact), list_fact)
        write_log(msg)
        return False
    list_expect = sorted(list(list_expect), key=sort_key)
    list_fact = sorted(list(list_fact), key=sort_key)
    if list_expect != list_expect:
        write_log('[WARN] diff, expect: {0},fact: {1}'.format(list_expect, list_fact))
        return False
    return True


def cmp_dict_list(expect_dict_list, fact_dict_list):
    result = cmp_list(expect_dict_list, fact_dict_list)
    if result:
        return True


def get_diff_set(set_expect, set_fact):
    result = True
    set_expect, set_fact = map(lambda x: set(x), (set_expect, set_fact))
    set_less = set_expect - set_fact
    set_more = set_fact - set_expect
    if set_less or set_more:
        result = False
    return result, set_more, set_less


def format_dict_data(origin_data, dict_parse):
    """
    将字典中内嵌的有字典组成的数组转化为字段放到根节点下,注意需要转化的字段一定是字典组成的数组
    :param origin_data: 原始字典
    :param dict_parse: 需要转化的数组字段名,多级以.间隔, 数组转化为字典依赖的主键字段,eg{'data.ads':'id'}
    :return: 转化后的字典new_dict
    """
    new_data = origin_data
    for k, v in dict_parse.items():
        list_k = k.split(".")
        parse_data = origin_data
        eval_expression = "new_data"
        key_name = "new_data"
        i = 0
        try:
            for c_k in list_k:
                i += 1
                if i < len(list_k):
                    eval_expression += "['{0}']".format(c_k)
                if i == len(list_k):
                    eval_expression += ".pop('{0}')".format(c_k)
                key_name += "['{0}']".format(c_k)
                parse_data = parse_data.get(c_k)
            eval(eval_expression)
            new_data[k] = {}
            for parse_dict in parse_data:
                if not isinstance(dict_parse, dict):
                    raise KeyError
                new_data[k][parse_dict.get(v)] = parse_dict
        except (KeyError, TypeError):
            write_log("{0} not exists, expression is : {1}".format(key_name, eval_expression), 'warn')
    return new_data


if __name__ == "__main__":


    expect = {"adType": "94", "orientation": "1", "countryCode": "CN", "imei": "0", "ad_backend_config": "8:toutiao_ios_Butterfly:3", "flow_tag_id": "128", "ad_backend": "8", "android_id": "0", "true_num": "1", "deviceBrand": "0", "platform": "2", "server_ip": "52.76.190.24", "unitId": "607", "ad_backend_data": "8:10895195759:1", "city_code": "7392", "client_ip": "39.109.124.93", "rand_value": "7345", "mac": "0", "idfa": "C98B99BB-1B2F-434E-BE53-FD651B03FB6A", "screensize": "375x667", "appId": "22050", "date": "2017-12-26 21:13:24", "networkType": "9", "osVersion": "10.3.1", "request_num": "1", "gaid": "0", "sdkVersion": "MI_2.9.7", "deviceModel": "iPhone8%2C1", "language": "en-JP", "created": "1514294004", "appVersionName": "8.3.4", "remoteIp": "39.109.124.93", "request_id": "5a424af369719457970000f6", "mcc_mnc": "44050", "publisherId": "5731"}
    fact   = {"adType": "94", "orientation": "1", "countryCode": "CN", "imei": "0", "ad_backend_config": "8:toutiao_ios_Butterfly:3", "flow_tag_id": "128", "ad_backend": "8", "android_id": "0", "true_num": "1", "deviceBrand": "apple", "platform": "2", "server_ip": "54.169.74.166", "unitId": "607", "ad_backend_data": "8:10895195759:1", "city_code": "7392", "client_ip": "39.109.124.93", "rand_value": "7345", "mac": "0", "idfa": "C98B99BB-1B2F-434E-BE53-FD651B03FB6A", "screensize": "375x667", "appId": "22050", "date": "2017-12-26 21:13:33", "networkType": "9", "osVersion": "10.3.1", "request_num": "1", "gaid": "0", "sdkVersion": "mi_2.9.7", "deviceModel": "iphone82c1", "language": "en-JP", "created": "1514294013", "appVersionName": "8.3.4", "remoteIp": "39.109.124.93", "request_id": "5a424af969719458a5a95826", "mcc_mnc": "0", "publisherId": "5731"}

    set_pass_adn_log = {"date", "sessionId", "request_id", "logId", "created", "server_ip", "useragent", "remoteIp", "time", "parentSessionId"}
    cmp_dict_data_pass_diff(expect, fact, set_pass=set_pass_adn_log)