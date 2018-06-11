# encoding:utf-8
import json
from file_utils import write_log
from business_url import get_url_params_dict
from cmp_utils import cmp_dict_data_pass_diff

SET_CHECK_NAME = {r"data.only_impression_url", r"data.ads.*.impression_url", r"data.ads.*.notice_url", "data.ads.*.click_url", r"data.ads.*.ad_tracking.*"}

def cmp_url():
    url_expect = raw_input("input the expect url: ").strip()
    url_fact = raw_input("input the expect url: ").strip()
    url_dict_expect = get_url_params_dict(url_expect, "url")
    url_dict_fact = get_url_params_dict(url_fact, "url")
    c_list_param = ["p", "mp", "q", "csp", "r"]
    for c_param in c_list_param:
        write_log(c_param.center(50, "="))
        cmp_dict_data_pass_diff(url_dict_expect.get(c_param), url_dict_fact.get(c_param))

if __name__ == "__main__":
    cmp_url()
