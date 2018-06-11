# encoding:utf-8
import re
import csv, os
import logging
import time
import json
from config import PRINT_LOG_LEVEL, DICT_LOG_KEYS
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
    if dict_log_level.get(log_level) >= PRINT_LOG_LEVEL:
        print(log_msg)
    if log_level == 'error':
        logging.error(log_msg)
    elif log_level == 'info':
        logging.info(log_msg)
    elif log_level == 'warn':
        logging.info(log_msg)
    else:
        logging.debug(log_msg)

if __name__ == '__main__':
    # write_log('yyy')
    read_csv_to_dict_list('../data/request_1_42_2.csv')