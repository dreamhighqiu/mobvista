# encoding:utf-8
from business_url import get_url_params_dict
from cmp_utils import cmp_dict_data_pass_diff
import requests
from file_utils import write_log, read_two_columns_csv_to_dict

def cmp_urls(url_name, expect_url, fact_url):
    list_params = ["p", "mp", "q", "csp", "r"]
    expect_url_dict = get_url_params_dict(expect_url, url_name)
    fact_url_dict = get_url_params_dict(fact_url, url_name)
    for param in list_params:
        write_log(param.center(20, "-"))
        expect_param_dict = expect_url_dict.get(param)
        fact_param_dict = fact_url_dict.get(param)
        cmp_dict_data_pass_diff(expect_param_dict, fact_param_dict)

if __name__ == "__main__":
    import json
    # mv
    url = 'http://{domain}/openapi/ad/v3?api_version=0.9&tnum=1&orientation=1&package_name=com.vstudio.camera360&install_ids=%5B177536538%5D&ad_type=94&ad_source_id=1&country_code=CN&timezone=GMT%252B09%253A00&mnc=50&ping_mode=1&category=0&native_info=%5B%7B"id"%3A2%2C"ad_num"%3A60%7D%5D&platform=2&cache2=51297.835938&unit_id=11542&os_version=11.1.2&sdk_version=MI_3.3.2&ttc_ids=%5B177536538%5D&req_type=1&exclude_ids=%5B177536538%5D&cache1=63937.039062&http_req=2&idfv=2603D94D-7465-4388-B0C3-BDFA40DCBE32&ad_num=60&app_version_name=8.3.4&screen_size=375.000000x812.000000&mcc=440&app_id=+90044&display_cids=%5B177536538%5D&idfa=C98B99BB-1B2F-434E-BE53-FD651B03FB6A&offset=0&only_impression=1&power_rate=80&sign=ad65e4be9a35160da6481391cff361fb&keyword=4MElRoztHFV0RaElinjso0vlRrJQYrxQh0RlG0veWvElRozMD%252B30RaElinRso0vlRrf2hbxXYZRlG0v0D%252Bf3HrdrwDXE8PV0WvElRozghdi0RaEl4MElRovlRretJoRlG0v0inv%2FinDAfAiBR0MpRovlRozsYrh0RaElRUDMWUjFiAhAi0RpRoSKogT%253D&language=en-JP&ui_orientation=26&version_flag=1&openidfa=74C87BBD-C675-EE2A-7651-6EBAC72835EA&ats=4MElRozGVTcsY7KbhTcBDrQThrcB4VeXDkxAR0v1RdxBJkVp6N%253D%253D&useragent=Mozilla%2F5.0%2520%28iPhone%253B%2520CPU%2520iPhone%2520OS%252010_2_1%2520like%2520Mac%2520OS%2520X%29%2520AppleWebKit%2F602.4.6%2520%28KHTML%252C%2520like%2520Gecko%29%2520Mobile%2F14D27%2520Camera360%2F8.3.4&model=iPhone8%252C1&sub_ip=192.168.6.233&network_type=9'
    # 3rd
    url = "http://{domain}/openapi/ad/v3?tnum=1&orientation=1&package_name=com.vstudio.camera360&install_ids=%5B177536538%5D&ad_type=94&ad_source_id=1&country_code=CN&timezone=GMT%252B09%253A00&mnc=50&ping_mode=1&category=0&native_info=%5b%7b%22id%22%3a2%2c%22ad_num%22%3a60%7d%5d&platform=2&cache2=51297.835938&unit_id=1341&os_version=11.1.2&sdk_version=MI_3.3.2&ttc_ids=%5B177536538%5D&req_type=1&exclude_ids=%5B177536538%5D&cache1=63937.039062&api_version=1.3&http_req=2&idfv=2603D94D-7465-4388-B0C3-BDFA40DCBE32&ad_num=60&app_version_name=8.3.4&screen_size=375.000000x812.000000&mcc=440&app_id=25259&display_cids=%5B177536538%5D&idfa=C98B99BB-1B2F-434E-BE53-FD651B03FB6A&offset=0&only_impression=1&power_rate=80&sign=34b5ffd843857e456693bd9e4fa52f62&keyword=4MElRoztHFV0RaElinjso0vlRrJQYrxQh0RlG0veWvElRozMD%252B30RaElinRso0vlRrf2hbxXYZRlG0v0D%252Bf3HrdrwDXE8PV0WvElRozghdi0RaEl4MElRovlRretJoRlG0v0inv%2FinDAfAiBR0MpRovlRozsYrh0RaElRUDMWUjFiAhAi0RpRoSKogT%253D&language=en-JP&ui_orientation=26&version_flag=1&openidfa=74C87BBD-C675-EE2A-7651-6EBAC72835EA&ats=4MElRozGVTcsY7KbhTcBDrQThrcB4VeXDkxAR0v1RdxBJkVp6N%253D%253D&useragent=Mozilla%2F5.0%2520%28iPhone%253B%2520CPU%2520iPhone%2520OS%252010_2_1%2520like%2520Mac%2520OS%2520X%29%2520AppleWebKit%2F602.4.6%2520%28KHTML%252C%2520like%2520Gecko%29%2520Mobile%2F14D27%2520Camera360%2F8.3.4&model=iPhone8%252C1&sub_ip=192.168.6.233&network_type=9"
    expect_domain = "test-net.rayjump.com"
    fact_domain = "test-adnet.rayjump.com"
    list_checks = ["only_impression_url", "impression_url", "notice_url", "click_url"]
    write_log(url.format(domain=expect_domain),"info")
    write_log(url.format(domain=fact_domain),"info")
    expect_res = requests.get(url.format(domain=expect_domain)).json()
    # write_log json.dumps(expect_res, indent=4)
    fact_res = requests.get(url.format(domain=fact_domain)).json()
    # write_log json.dumps(fact_res, indent=4)
    if expect_res.get("status") == fact_res.get("status") and fact_res.get("status") == 1:
        list_expect_campaign = expect_res.get("data").get("ads")
        list_fact_campaign = fact_res.get("data").get("ads")
        set_expect_ids = set([_.get("id") for _ in list_expect_campaign])
        set_fact_ids = set([_.get("id") for _ in list_fact_campaign])
        list_campaign_id = list(set_expect_ids.intersection(set_fact_ids))
        if list_campaign_id:
            campaign_id = list_campaign_id[0]
            expect_campaign = [_ for _ in list_expect_campaign if _.get("id") == campaign_id][0]
            fact_campaign = [_ for _ in list_fact_campaign if _.get("id") == campaign_id][0]
            expect_campaign["only_impression_url"] = expect_res.get("data").get("only_impression_url")
            fact_campaign["only_impression_url"] = fact_res.get("data").get("only_impression_url")
            for check_url in list_checks:
                write_log(check_url.center(50, '='))
                c_expect_url = expect_campaign.get(check_url)
                c_fact_url = fact_campaign.get(check_url)
                write_log("expect_url: %s"%c_expect_url)
                write_log("fact_url: %s"%c_fact_url)
                cmp_urls(check_url, c_expect_url, c_fact_url)





