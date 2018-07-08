# encoding:utf-8
import re
import csv, os
import logging
import time
import json
from os import popen
MUST_PATTERN = re.compile(r'^\[')
is_init_log = False


def read_file(file_type, return_type, file_path):
    if file_type == "csv":
        if return_type == "dict":
            return read_two_columns_csv_to_dict(file_path)
        elif return_type == "list":
            return read_to_columns_csv_to_list(file_path)
    elif file_type == "json":
        return read_txt_to_dict(file_path)
    else:
        with open(file_path) as rf:
            return rf.read()


def read_txt_to_list(file_path, remove_line_remark=True, remove_line_break=True, remove_line_empty=True):
    """
    将txt文件读取出来转化成列表
    :param file_path: 文件路径
    :param remove_line_remark: 是否去掉备注行，#开头的行为备注行
    :param remove_line_break: 是否去掉末尾的换行符
    :param remove_line_empty: 是否去掉空行
    :return:
    """
    with open(file_path) as rf:
        list_all = rf.readlines()
    lb_remark = lambda x: True if x.startswith('#') and remove_line_remark else False
    lb_break = lambda x: x[:-1] if x.endswith('\n') and remove_line_break else x
    lb_empty = lambda x: True if len(x.replace(' ', '').replace('\n', '')) == 0 else False
    list_final = [lb_break(_) for _ in list_all if not (lb_remark(_) or lb_empty(_))]
    return list_final

def get_new_file(file_path):
    try:
        command = "find %s -type f -mmin -1"%file_path
        log_file_list = popen(command).readlines()
        log_file = log_file_list[0]
        return log_file
    except StandardError as e:
        write_log("get the latest file failed: %s"%e)
        return ""


def read_txt_to_dict(file_path):
    """
    将txt文件读取出来转化成字典
    :param file_path: 文件路径
    :return:
    """
    dict_data = {}
    with open(file_path) as rf:
        data = rf.read()
    data = data.replace("\t", "").replace("\n", "").replace("\r", "")
    try:
        dict_data = json.loads(data)
    except ValueError:
        write_log("data is  wrong, please check: {0}".format(file_path), "error")
    return dict_data


def read_csv_to_dict_list(file_path, name_index=0, limit_row=0, limit_column=0):
    csv_reader = csv.reader(open(file_path))
    index = 0
    list_result = []
    dict_name_value = {}
    for row in csv_reader:
        if index < name_index:
            continue
        name = row[name_index]
        list_value = row[name_index+1: limit_column+1]
        for value in list_value:
            pass
        index += 1
        if index == limit_row:
            break
    # for name, list_value in dict_name_value.values():
    #     list_result


def read_two_columns_csv_to_dict(file_path):
    # 适用于只有两列，第一列转为key, 第二列转为value
    csv_reader = None
    dict_data = {}
    try:
        csv_reader = csv.reader(open(file_path))
    except Exception as e:
        write_log(e, 'error')
    if not csv_reader:
        write_log("The file is empty: %s" % file_path, "warn")
    else:
        for k, v in csv_reader:
            if k.startswith("#"):
                continue
            dict_data[k] = v.replace("%2c",",")
    return dict_data


def read_to_columns_csv_to_list(file_path, limit_row=0, limit_column=0):
    # 适用于只有两列的csv
    csv_reader = []
    list_data = []
    try:
        csv_reader = csv.reader(open(file_path))
    except Exception as e:
        write_log(e, 'error')
    if not csv_reader:
        write_log("The file is empty: %s" % file_path, "warn")
    else:
        for each in csv_reader:
            if each[0].startswith("#"):
                continue
            list_data.append(each)
    return list_data


def init_log():
    file_name = 'report/%s.log' % '%d-%d-%d-%d'%time.localtime()[:4]
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=file_name,
                        filemode='a+')


dict_log_level = {
    "info": 2,
    "debug": 1,
    "warn": 3,
    "error": 4
}

def write_log(log_msg, log_level='debug'):
    global is_init_log
    if not is_init_log:
        init_log()
        is_init_log = True
    #if dict_log_level.get(log_level) >= PRINT_LOG_LEVEL:
        print(log_msg)
    if log_level == 'error':
        logging.error(log_msg)
    elif log_level == 'info':
        logging.info(log_msg)
    elif log_level == 'warn':
        logging.info(log_msg)
    else:
        logging.debug(log_msg)

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





if __name__ == '__main__':
    
    list1=[1, 2, 3, 4, 5,6]
    list2=[2, 4, 5, 67, 7]
    print(cmp_dict_list(list1, list2)
)