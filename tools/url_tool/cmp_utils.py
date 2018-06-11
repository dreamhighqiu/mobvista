# encoding:utf-8

from file_utils import *
import json
RESULT = True
SET_DIFF_PARAM = set()
from business_url import get_url_params_dict


def cmp_dict_data_pass_diff(expect_dict, fact_dict, key_prefix="", set_pass=set(), set_diff=set(),
                            set_more=set(), set_less=set(), first_round=True, set_check_url=set(), mode=1):
    global SET_DIFF_PARAM, RESULT
    if first_round:
        SET_DIFF_PARAM = set()
        RESULT = True
    result = RESULT
    if expect_dict == fact_dict:
        return True, set()
    if not set_pass:
        set_pass = set()
    if not (expect_dict and fact_dict) or not(isinstance(expect_dict, dict) and isinstance(fact_dict, dict)):
        SET_DIFF_PARAM.add('illegal data')
        write_log('one side data is illegal, \n\texpect: {0}\t{1}\n\tfact:{2}\t{3}'.format(type(expect_dict), expect_dict, type(fact_dict), fact_dict), 'warn')
        return False, set()
    set_expect_keys = set(expect_dict.keys())
    set_fact_keys = set(fact_dict.keys())
    set_cmp = set_expect_keys.union(set_fact_keys)
    for key in set_cmp:
        pass_this = False
        c_result = True
        cmp_key = str(key)
        if key_prefix:
            cmp_key = '{0}{1}'.format(key_prefix, key)
        for set_pass_key in set_pass:
            match_pass = re.match(set_pass_key, cmp_key)
            if match_pass and len(match_pass.group()) == len(cmp_key):
                pass_this = True
                break
        if pass_this:
            continue

        # if remove_str_digit(cmp_key) in set_pass:
        #     continue
        expect_v = expect_dict.get(key)
        fact_v = fact_dict.get(key)
        for check_key in set_check_url:
            match_check = re.match(check_key, cmp_key)
            if match_check:
                if len(match_check.group()) == len(cmp_key):
                    expect_v = get_url_params_dict(expect_v, cmp_key)
                    fact_v = get_url_params_dict(fact_v, cmp_key)
                break
        if expect_v != fact_v:
            if not isinstance(expect_v, dict):
                c_result = False
                SET_DIFF_PARAM.add(cmp_key)
                if not c_result:
                    try:
                        write_log('{0}:\n\texpect is : {1} {2}\n\tfact   is : {3} {4}'
                                  .format(cmp_key, type(expect_v), expect_v, type(fact_v), fact_v), 'warn')
                    except Exception as e:
                        write_log('{0}:\n\texpect is : {1}\n\tfact   is : {2}'
                                  .format(cmp_key, type(expect_v), type(fact_v)), 'error')
                        write_log(e, 'error')
            if type(expect_v) == type(fact_v) and isinstance(expect_v, dict):
                c_result, x = cmp_dict_data_pass_diff(expect_v, fact_v, cmp_key+'.', set_pass, set_diff,
                            set_more, set_less, first_round=False, set_check_url=set_check_url)
            result = result and c_result
        RESULT = RESULT and result
    return RESULT, SET_DIFF_PARAM

def cmp_dict_new(expect, fact, cmp_keys):
    k_expect = set(expect.keys())
    k_fact = set(fact.keys())
    base_keys = k_expect.union(k_fact)
    for k in base_keys:
        for ck in cmp_keys:
            match_check = re.match(ck, k)
            if match_check:
                cmp_dict_data_pass_diff(expect.get(k), fact.get(k), k)
                break





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
            write_log(msg, 'warn')
    return result, list_diff


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

def lower_dict_key(odict):
    for k in odict.keys():
        if not k.islower():
            odict[k.lower()] = odict[k]
            odict.pop(k)
    return odict


if __name__ == "__main__":
    true = True
    false = False
    null = None
    expect_dict = raw_input("input expect data: \n")
    fact_dict = raw_input("input fact data: \n")
    cmp_dict_data_pass_diff(eval(expect_dict),eval(fact_dict)) 
