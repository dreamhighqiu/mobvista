# encoding:utf-8

import json
from scripts.backend.backend import AdBackend
from scripts.common.file_utils import write_log
from scripts.common.cmp_utils import cmp_dict_data_pass_diff, format_dict_data


def render_response(interface_type, backend_id, index_list, show_param_list, send_urls=False, set_domain = set()):
    """
    根据传入的参数拼装请求获取返回并检验
    :param interface_type: 接口类型，v3-sdk  ads-online api
    :param backend_id: 后端id， 0-adn_net 1-midway 2-imobile 3-adinall 4-inmobi 5-smatto 6-pubnative 7-leiting
    :param index_list: 请求的数据所在文件名 data/$interface_type/$backend/request_$index.csv
    :param show_param_list: 需要打印的字段信息
    :param send_urls： 是否发送返回的url
    :return:
    """
    ab = AdBackend(interface_type, backend_id)
    for index in index_list:
        ab.check_my_response(index, False, set_pass=["data.session_id", "data.parent_session_id"])
        ad_data = ab.response.get('data')
        if not ad_data:
            continue
        # ab.mp_url_list.append(ad_data.get('only_impression_url').replace('https', 'http'))
        campaign_list = ad_data.get('ads')
        if campaign_list:
            for campaign in campaign_list:
                if len(campaign.get('impression_url').split('k=')) > 1:
                    write_log("impKey is: %s" % campaign.get('impression_url').split('k=')[1].split('&')[0])
                else:
                    write_log("can't get impKey from impression_url", 'error')
                if campaign.get('notice_url') and len(campaign.get('notice_url').split('k=')) > 1:
                    write_log("clkKey is: %s" % campaign.get('notice_url').split('k=')[1].split('&')[0])
                elif campaign.get('click_url') and len(campaign.get('click_url').split('k=')) > 1:
                    write_log("clkKey is: %s" % campaign.get('click_url').split('k=')[1].split('&')[0])
                else:
                    write_log("can't get clkKey from notice_url or click_url", 'error')
                write_log('show offer param details:')
                for param in show_param_list:
                    if param in ad_data.keys():
                        param_value = ad_data.get(param)
                    else:
                        param_value = campaign.get(param)
                    if isinstance(param_value, dict):
                        param_value = json.dumps(param_value, indent=4)
                    write_log("%s is: %s" % (param, param_value))
                    # if isinstance(param_value, unicode):
                    #     write_log("%s is: %s" % (param, param_value+"&is_video=3"))
                write_log('-'*150)
            if send_urls:
                ab.send_tracking(ad_data, set_domain)
    return ab.response

def cmp_response(req_index_list, expect_bid=0, fact_bid=1, req_type="v3", show_list={"id"}, set_domain={"test-net.rayjump.com"}):
    # index_list = ["1_42_3_online"]
    expect_bid = 0
    fact_bid = 1
    set_pass = []
    # 需要打印的offer信息
    expect_res = render_response(req_type, expect_bid, req_index_list, show_list, False, set_domain)
    fact_res = render_response(req_type, fact_bid, req_index_list, show_list, False, set_domain)
    # adserver_id = adserver_res["data"]["ads"][0]["id"]
    expect_res = format_dict_data(expect_res, {"data.ads": "id"})
    fact_res = format_dict_data(fact_res, {"data.ads": "id"})
    cmp_dict_data_pass_diff(expect_res, fact_res, set_pass=set_pass)
    # corsair_res = render_response(interface_type, corsair_backend_id, index_list, show_param_list, True, set_domain)
    # corsair_res["data"]["ads"][0]["id"] = adserver_id
    # for i in range(len(corsair_res["data"]["ads"])):
    #     corsair_res["data"]["ads"][i]["id"] = int(corsair_res["data"]["ads"][i]["id"])

    # set_pass = {"data.session_id", "data.parent_session_id"}
    # cmp_dict_data_pass_diff(adserver_res, corsair_res, set_pass=set_pass)

if __name__ == "__main__":
    # interface_type = "ads"
    # index_list = ["2"]
    interface_type = "v3"
    index_list = ["1_94_3"]
    # index_list = ["1_42_3_online"]
    expect_bid = 0
    fact_bid = 1
    set_domain = {"tuchuan-net.rayjump.com","test-mtrack.rayjump.com"}
    show_param_list = {"id", "endcard_url", "endscreen_url"}
    # cmp_response(index_list, show_list=show_param_list)
    render_response(interface_type, expect_bid, index_list, show_param_list, True, set_domain)