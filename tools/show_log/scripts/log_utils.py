# encoding:utf-8
from config import DICT_LOG_KEYS
from file_utils import write_log, read_txt_to_list, get_new_file


def get_log_new(file_path, key_name):
    log_file = get_new_file(file_path)
    if not log_file:
        write_log("The file folder is empty or no file updated in 1 minute: %s"%file_path, "warn")
        return {},[]
    log_file = log_file[:-1]
    print("The full log path is: %s"%log_file, "info")
    log_value = read_txt_to_list(log_file)
    if not log_value:
        write_log("The file is empty: %s"%log_file, "warn")
        return {},[]
    list_values = log_value[-1].split("\t")
    list_keys = DICT_LOG_KEYS.get(key_name)
    if len(list_values) != len(list_keys):
        write_log("the length of log key:%s is diff to vlue: %s"%(len(list_keys), len(list_values)), "warn")
    return dict(zip(list_keys, list_values)), list_keys

