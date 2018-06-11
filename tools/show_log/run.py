# encoding:utf-8
from config import DICT_LOG_MAP
from scripts.log_utils import get_log_new
from scripts.cmp_utils import cmp_dict_data_pass_diff
from time import sleep
from scripts.log_utils import write_log
import json


def show_log(log_type, check_detail=False):
    log_path, log_key = DICT_LOG_MAP.get(log_type)
    dict_log, list_keys = get_log_new(log_path, log_key)
    if dict_log:
        write_log("output by order".center(50, "-"))
        for k in list_keys:
            write_log((k, dict_log.get(k)))
        write_log("output by json".center(50, "-"))
        write_log(json.dumps(dict_log))
    while dict_log and check_detail:
        key_name = raw_input("input the param you wanna check, 0 to stop: ")
        if key_name == "0" or len(key_name) == 0:
            break
        # write_log(dict_log.get(key_name))
    return dict_log


def compare_log(expect_log_type, fact_log_type):
    write_log("search expect log".center(50, '-'))
    dict_expect_log = show_log(expect_log_type)
    sleep(1)
    write_log("waiting for 1 seconds to get fact data")
    write_log("search fact log".center(50, '-'))
    dict_fact_log, _ = show_log(fact_log_type)
    if dict_fact_log and dict_expect_log:
        cmp_dict_data_pass_diff(dict_expect_log, dict_fact_log)
    else:
        print("expect or fact log dose not exist")


def check_stop(info):
    write_log(info)
    input_str = raw_input("1-continue|0-back|#-over|*-show log_types: ").strip()
    if input_str == "*":
        write_log("the log type provided as below:\n\t%s"%(json.dumps(DICT_LOG_MAP, indent=4)), "info")
    if input_str == "#":
        raise SystemExit
    elif input_str != "1":
        return True
    return False


def check_input(input_str, input_range):
    while 1:
        input_value = raw_input(input_str).strip()
        if input_value not in input_range:
            write_log("err input, you can only choose these: \n%s"%"\n\t".join(input_range), "warn")
            continue
        return input_value


def run():
    action_type = check_input("choose mode, 1-show_log|2-cmp_log: ", ["1", "2"])
    while 1:
        write_log("the log type provided as below:\n\t%s"%(json.dumps(DICT_LOG_MAP, indent=4)), "info")
        while 1:
            if action_type == "1":
                expect_log = check_input("choose log_type: ", DICT_LOG_MAP.keys())
                while 1:
                    show_log(expect_log, False)
                    if check_stop("continue search current log_type"):
                        break
            else:
                expect_log = check_input("choose expect log_type: ", DICT_LOG_MAP.keys())
                fact_log = check_input("choose fact log_type: ", DICT_LOG_MAP.keys())
                while 1:
                    compare_log(expect_log, fact_log)
                    if check_stop("do you wanna continue current log_type"):
                        break
            if check_stop("do you wanna continue current interface"):
                break
        if check_stop("do you wanna continue current action"):
            break

if __name__ == "__main__":
    run()
