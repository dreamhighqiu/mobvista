# encoding:utf-8
import time
from config import DICT_LOG

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
    log_time = dict_log_time.get('{cur_hour}')
    dict_replace = {}
    if log_type:
        dict_replace.setdefault('{log_type}', log_type)
    dict_replace.update(**dict_log_time)
    list_param_name = []
    if not DICT_LOG.get(server_type):
        print('[WARN] the server_type {0} you choose is not exists, please check you config!!!'.format(server_type))
        return "", "", "", ""
    root_path = DICT_LOG.get(server_type).get('root_path')
    log_path = DICT_LOG.get(server_type).get('log_path')
    log_param_path = DICT_LOG.get(server_type).get('log_params_path')
    for k, v in dict_replace.items():
        log_path = log_path.replace(k, v)
        log_param_path = log_param_path.replace('{%s}' % k, v)
    if log_param_path:
        with open(log_param_path) as rf:
            list_param_name = rf.readlines()
        list_param_name = [_.replace('\n', '')[:-1] for _ in list_param_name if not _.startswith('#')]
        print(root_path, log_path, list_param_name, log_time)
    return root_path, log_path, list_param_name, log_time

get_log_info("1","adn_net")
