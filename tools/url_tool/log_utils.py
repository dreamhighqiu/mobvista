# encoding:utf-8
import time
from cmp_utils import cmp_dict_data_pass_diff
from file_utils import write_log, read_txt_to_list, get_new_file
from config import DICT_LOG, DICT_LOG_SEARCH, DICT_LOG_KEYS
import os

def get_log_new(file_path, key_name):
    log_file = get_new_file(file_path)
    if not log_file:
        return {}
    log_value = read_txt_to_list(file_path+log_file)
    if not log_value:
        return {}
    list_values = log_value[-1].split("\t")
    list_keys = DICT_LOG_KEYS.get(key_name)
    if len(list_values) != len(list_keys):
        write_log("the length of log key:%s is diff to vlue: %s"%(len(list_keys), len(list_values)))
    return dict(zip(list_keys, list_values))

def get_log(server_type, log_type, via_type, via_info):
    """
    获取单个接口末尾行日志，以map形式输出
    :param server_type: 服务端类型,如1-adn_net，2-midway_server，3-midway_tracking
    :param log_type: 接口类型，如request，impression，click，only_impression,install等
    :param via_type: 匹配日志的方式 1-通过关键字  2-通过行号
    :param via_info: via_type的1则via_info为  via_type=2则为行号
    :return: 匹配的接口日志行信息
    """
    root_path, log_path, log_key = get_log_info(server_type, log_type)
    if not root_path:
        # write_log("get log path failed, server_type: {0}, log_type: {1}".format(server_type, log_type))
        return {}
    if int(via_type) == 1:
        list_via_info = via_info.split("+")
        cmd = 'cat {0}'.format(log_path)
        for each_via_info in list_via_info:
            cmd += "| grep {1}".format(each_via_info)
        try:
            log_lines = [_[:-1] for _ in os.popen(cmd).readlines() if len(_) > 0]
            if len(log_lines) < 1:
                raise None
            list_param_value = log_lines[0].split("\t")
        except StandardError:
            write_log("get log failed , not exists or not unique, via {0}".format(cmd), 'warn')
            return {}
    else:
        try:
            log_lines = [_[:-1] for _ in read_txt_to_list(log_path) if len(_) > 0]
            if len(log_lines) < int(via_info):
                raise None
            list_param_value = log_lines[int(via_info)].split("\t")
        except StandardError, e:
            write_log("get log failed , file_path: {0}, msg: {1}".format(log_path, e), 'warn')
            return {}
    list_param_name = DICT_LOG_KEYS.get(log_key)
    if len(list_param_value) != len(list_param_name):
                write_log('param size is wrong,\n\texpect is {0}; fact is {1}\n\tplease check {2}!!!'
                          .format(len(list_param_name), len(list_param_value),
                                  DICT_LOG.get(server_type).get('log_params_path')), 'warn')

    return dict(zip(list_param_name, list_param_value))


def cmp_log(key_expect="", key_fact="", list_log_type="all", via_line=False):
    if list_log_type == "all":
        list_log_type = DICT_LOG_SEARCH.keys()
    for log_type in list_log_type:
        log_action = DICT_LOG_SEARCH.get(log_type)
        list_log_type = DICT_LOG_SEARCH.keys()
        if not log_action:
            write_log("The log_type {0} is not in the config, please check!".format(log_type), 'warn')
            continue
        write_log('start to cmp_log {0}'.format(log_type), 'info')
        if via_line:
            # 如果不是查询所有的，那么以为着没有获取到广告，则不用
            log_action["expect"][3] = -2
            log_action["expect"][2] = 2
            log_action["fact"][3] = -1
            log_action["fact"][2] = 2
        else:
            log_action["expect"][3] += key_expect
            log_action["fact"][3] += key_fact
        log_expct = apply(get_log, tuple(log_action.get("expect")))
        log_fact = apply(get_log, tuple(log_action.get("fact")))
        cmp_dict_data_pass_diff(log_expct, log_fact, log_action.get("pass"))


def get_log_time(check_time=""):
    """
    刷新时间，如果用户不输入时间，则获取当前时间
    :param check_time:
    :return:
    """
    if not check_time:
        now = time.localtime()
        check_time = time.strftime('%Y-%m-%d-%H', now)
    list_info = check_time.split('-')
    year, month, date, hour = list_info
    cur_month = '{0}-{1}'.format(year, month)
    cur_date = '{0}-{1}'.format(cur_month, date)
    cur_hour = '{0}-{1}'.format(cur_date, hour)
    dict_log_time = dict(zip(['{year}', '{month}', '{date}', '{hour}', '{cur_month}', '{cur_date}', '{cur_hour}'],
                             [year, month, date, hour, cur_month, cur_date, cur_hour]))
    return dict_log_time


def get_log_info(server_type, log_type="", check_time=""):
    dict_log_time = get_log_time(check_time)
    dict_replace = {}
    if log_type:
        dict_replace.setdefault('{log_type}', log_type)
    dict_replace.update(**dict_log_time)
    if not DICT_LOG.get(server_type):
        write_log('the server_type {0} you choose is not exists, please check you config!!!'.format(server_type), 'warn')
        return "", "", "", ""
    root_path = DICT_LOG.get(server_type).get('root_path')
    log_path = DICT_LOG.get(server_type).get('log_path')
    log_key = DICT_LOG.get(server_type).get('log_key')
    for k, v in dict_replace.items():
        log_path = log_path.replace(k, v)
    return root_path, log_path, log_key


"""
key_word 5aaa53d64e5242519a8ebcb4
获取corsair request日志
get_log("corsair", "request", 1, keyword)
get_log("corsair", "request", 2, -1)

获取adnet request日志
get_log("adnet", "request", 1, keyword)
get_log("adnet", "request", 2, -1)

获取adn_net request日志
get_log["stat_v3", "request", 1, keyword)
get_log["stat_v3", "request", 2, -1)

获取adn_net pv日志
get_log["stat_v3", "only_impression", 1, keyword)
get_log["stat_v3", "only_impression", 2, -1)

获取adn_net imp日志
get_log["stat_v3", "impression", 1, keyword)
get_log["stat_v3", "impression", 2, -1)

获取adn_net notice日志
get_log["stat_v3", "click", 1, keyword)
get_log["stat_v3", "click", 2, -1)

获取adn_net tracking_report日志
get_log["stat_v3", "tracking", 1, "play_percentage+\"rate\":\"0\"+"+keyword)
get_log["stat_v3", "tracking", 1, "play_percentage+\"rate\":\"25\"+"+keyword)
get_log["stat_v3", "tracking", 1, "play_percentage+\"rate\":\"50\"+"+keyword)
get_log["stat_v3", "tracking", 1, "play_percentage+\"rate\":\"75\"+"+keyword)
get_log["stat_v3", "tracking", 1, "play_percentage+\"rate\":\"100\"+"+keyword)

获取adn_net tracking_no_report日志
get_log["stat_v3", "tracking", 1, "close+"+keyword)
get_log["stat_v3", "tracking", 1, "endcard_show+"+keyword)
get_log["stat_v3", "tracking", 1, "unmute+"+keyword)
get_log["stat_v3", "tracking", 1, "mute+"+keyword)
"""