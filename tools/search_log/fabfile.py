# encoding:utf-8

from fabric.api import env, run, settings, hide
import log_utils
import json
from config import HOST, DICT_LOG
env.hosts = HOST


def read_me(info_type="1"):
    """
    查看帮助文档  1-查看使用说明|2-查看配置文件|3-查看函数介绍
    :param info_type:
    :return:
    """
    if info_type == "1":
        print("""
        函数介绍
        1）show_one
        查询指定服务端的某个接口的日志的关键字行
        调用实例1，动态录入参数： fab show_one
        调用实例2, 指定参数：  fab show_one:1,request,59e09957fe1f655266a5bea0或者fab show_one
        -----------------------------------------------------------------------------------------
        参数介绍：
        :param server_type: 服务端类型1-adn_net，2-midway_server，3-midway_tracking
        :param log_type: 接口日类型，如request，impression，click，only_impression,install等
        :param keyword: 匹配日志行的关键字，一般按照requestId来查找，如59df1c54fe1f65692c0076ba
        :param show_detail: 是否展示日志细节，True将字段名和值一一输出，False则不查询细节字段
        :param check_time:日志时间，如果不传取默认值表示当前时间，传入格式为2017-10-09-15
        :return: 匹配的日志行信息
        =========================================================================================
        2）show_tail
        查询指定服务端的某种接口日志的末尾行
        调用实例1，动态录入参数： fab show_tail
        调用实例2，指定参数： fab show_tail:server_type,log_type,log_line=1,check_time=""
        -----------------------------------------------------------------------------------------
        参数介绍：
        :param server_type:服务端类型,如1-adn_net，2-midway_server，3-midway_tracking
        :param log_type:接口类型，如request，impression，click，only_impression,install等
        :param check_time:日志时间，如果不传取默认值表示当前时间，传入格式为2017-10-09-15
        :return:匹配的日志行信息
        =========================================================================================
        3）show_all
        查询某个服务所有接口的日志
        调用实例1，动态录入参数：fab show_all
        调用实例2，指定参数： fab show_all:1,59df1c54fe1f65692c0076ba,2017-09-10-13
        -----------------------------------------------------------------------------------------
        参数介绍：
        :param server_type:服务端类型1-adn_net，2-midway_server，3-midway_tracking
        :param keyword:匹配日志行的关键字，一般按照requestId来查找，如59df1c54fe1f65692c0076ba
        :param check_time:日志时间，传入格式为2017-10-09-15，如果不传取默认值表示当前时间
        :return:匹配日志行信息
        """)
    elif info_type == "2":
        print('服务端日志配置信息如下:')
        print('查询的服务器：{0}'.format(HOST))
        print(json.dumps(DICT_LOG, indent=4))
    else:
        print("""
        配置说明
            1）config.py用于录入配置信息
            2）HOST用于配置服务所在的机器IP，可多个，程序会自动轮询多台服务器
            3）DICT_LOG用于配置服务端日志路径，如果您要增加查询接口，请在此处添加即可
            ------------------------------------------------------------------
            参数介绍
            log_name: 服务端类型
            root_path: 服务日志的根路径
            log_path: 接口日志的路径模板
            log_params_path: 接口日志的字段名称
        """)


def show_one(server_type="", log_type="", keyword="", show_detail="", check_time=""):
    """
    fab show_one--查询指定服务端指定接口的日志关键字行
    :param server_type: 服务端类型,如1-adn_net，2-midway_server，3-midway_tracking
    :param log_type: 接口类型，如request，impression，click，only_impression,install等
    :param keyword: 匹配日志行的关键字，一般按照requestId来查找，如59df1c54fe1f65692c0076ba
    :param show_detail: 是否展示日志细节，True将字段名和值一一输出
    :param check_time:日志时间，传入格式为2017-10-09-15，如果不传取默认值表示当前时间
    :return: 匹配的接口日志行信息
    """
    dict_log_detail = {}
    while not server_type:
        print('server_type enum as below:')
        for server_type in sorted(DICT_LOG.keys()):
            print('{0}  {1}'.format(server_type, DICT_LOG.get(server_type).get('log_name')))
        server_type = raw_input('please choose server_type: ').strip()
    while not log_type:
        log_type = raw_input('please input the log_type you wanna search: ').strip()
    while not keyword:
        keyword = raw_input("please input the keyword you wanna search: ").strip()
    while show_detail == "":
        show_detail = int(raw_input("do you wanna show log detail, 1-yes|0-no: ").strip())
    while check_time and len(check_time.split('-')) < 4:
        check_time = raw_input("please input the log_time you wanna search, like 2017-09-10-13: ").strip()
    while keyword:
        root_path, log_path, list_param_name, log_time = log_utils.get_log_info(server_type, log_type, check_time)
        if not root_path:
            break
        command = "grep '{0}' {1} ".format(keyword, log_path)
        with settings(hide('warnings', 'stderr'), warn_only=True):
            res = run(command)
        if show_detail and res.find("No such file or directory") < 0:
            list_value = res.split('\t')
            if len(list_value) != len(list_param_name):
                print('[ERROR] param size is diff to value size, please check the log_params_path ref file!!!')
                raise SystemExit
            set_kv = zip(list_param_name, list_value)
            dict_log_detail = dict(set_kv)
            for i in set_kv:
                print(i)
        # 如果指定时间或者有其他方法调用则结束循环
        if check_time:
            break
        keyword = raw_input("please input the keyword you wanna search, enter to end: ").strip()
    return dict_log_detail


def show_tail(server_type="", log_type="", log_line="f", check_time=""):
    """
    fab show_tail--查询指定服务端只当接口的日志末尾行
    :param server_type:服务类型,如1-adn_net，2-midway_server，3-midway_tracking
    :param log_type:接口类型，如request，impression，click，only_impression,install等
    :param check_time:日志时间，传入格式为2017-10-09-15，如果不传取默认值表示当前时间
    :return:匹配的日志行信息
    """
    while not server_type:
        print('server_type enum as below:')
        for server_type in sorted(DICT_LOG.keys()):
            print('{0}  {1}'.format(server_type, DICT_LOG.get(server_type).get('log_name')))
        server_type = raw_input('please choose server_type: ').strip()
    while not log_type:
        log_type = raw_input('please input the log_type you wanna search: ').strip()
    log_line = raw_input('input the tail line num you wanna show, a int or f, default f: ')
    if not log_line:
        log_line = "f"
    while check_time and len(check_time.split('-')) < 4:
        check_time = raw_input("please input the log_time you wanna search, like 2017-09-10-13: ").strip()
    while log_type:
        root_path, log_path, list_param_name, log_time = log_utils.get_log_info(server_type, log_type, check_time)
        if not root_path:
            break
        command = "tail -{0} {1}".format(log_line, log_path)
        with settings(hide('warnings', 'stderr'), warn_only=True):
            run(command)
        log_type = raw_input("please input the log_type you wanna search, enter to end: ").strip()


def show_all(server_type="", keyword="", show_detail="", check_time=""):
    """
    fab show_all--查询指定服务端所有接口的关键字行
    调用实例 fab show_all:1,59df1c54fe1f65692c0076ba,2017-09-10-13
    :param server_type:服务端类型1-adn_net，2-midway_server，3-midway_tracking
    :param keyword:匹配日志行的关键字，一般按照requestId来查找，如59df1c54fe1f65692c0076ba
    :param check_time:日志时间，传入格式为2017-10-09-15，如果不传取默认值表示当前时间
    :return:匹配日志行信息
    """

    dict_log_details = {}
    while not server_type:
        print('server_type enum as below:')
        for server_type in sorted(DICT_LOG.keys()):
            print('{0}  {1}'.format(server_type, DICT_LOG.get(server_type).get('log_name')))
        server_type = raw_input('please choose server_type: ').strip()
    while not keyword:
        keyword = raw_input("please input the keyword you wanna search: ").strip()
    while not show_detail:
        show_detail = int(raw_input("do you wanna show log detail, 1-yes|0-no: ").strip())
    while check_time and len(check_time.split('-')) < 4:
        check_time = raw_input("please input the log_time you wanna search, like 2017-09-10-13: ").strip()
    while keyword:
        root_path, log_path, list_param_name, log_time = log_utils.get_log_info(server_type, check_time)
        if not root_path:
            break
        command = "ls {0}".format(root_path)
        with settings(hide('running', 'stdout', 'stderr'), warn_only=True):
            str_log_type = run(command)
        if str_log_type.find('No such file or directory') >= 0:
            print('[ERROR] The root path is not exsits, please check the config.py!!!')
            raise SystemExit
        str_log_type = str_log_type.replace('\n', '|').replace('\t', '|').replace('\r', '|').replace(' ', '|').split('|')
        list_log_type = sorted([_ for _ in str_log_type if _])
        for log_type in list_log_type:
            print(log_type.center(50, '-')+"\n")
            dict_log_detail = show_one(server_type, log_type, keyword, show_detail, log_time)
            if show_detail and dict_log_detail:
                dict_log_details.setdefault(log_type, dict_log_detail)
        if show_detail:
            param_name = raw_input("please input the param_name you wanna check, enter to end: ")
            while param_name:
                for log_type in dict_log_details.keys():
                    print(log_type, dict_log_details.get(log_type).get(param_name))
                print('-'*20)
                param_name = raw_input("please input the param_name you wanna check, enter to end: ").strip()
        keyword = raw_input("please input the keyword you wanna search, enter to end: ").strip()

