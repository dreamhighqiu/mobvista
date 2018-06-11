# encoding:utf-8
from urllib import urlencode
from check_reponse.scripts.common.file_utils import read_csv_to_list, write_log
from check_reponse.scripts.common.request_utils import GetResponse
import json
import requests

"""
smatto召回接口
"""

"""
smatto
offer.title = SNAST.adtitle
offer.desc = SNAST.adtext
offer.ctatext = SNAST.ctatext
offer.icon_url = SNAST.iconimage.url
offer.image_url = SNAST.mainimage.url
offer.click_url = SNAST.clickUrl
offer.ad_url_list = beacons
"""

# video
"""http://soma.smaato.net/oapi/reqAd.jsp?adspace=3090&pub=0&devip=39.109.124.93&device=Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36&googleadid=ee94a9ba-c079-4786-8867-2ab109ed5610&googlednt=true&androidid=ccf785f98e92d84b&vastver=2&format=video&videotype=outstream&response=XML&formatstrict=true"""

class Smatto:
    def __init__(self, host="soma.smaato.net", file_index="1"):
        self.url = "http://{0}/mobvistaNativeWd?{1}"
        self.host = host
        self.data_path = "../../data/leiting/"
        self.request_file_name = "request_{0}.csv".format(file_index)
        self.response_file_name = "response_{0}.json".format(file_index)
        self.res = None

    def build_request_url(self):
        query_data = {}
        write_log(u"开始读取请求数据所在的文件：{0}".format(self.data_path + self.request_file_name))
        request_params = read_csv_to_list(self.data_path + self.request_file_name)
        if not request_params:
            write_log(u"读取文件失败!!!", "error")
        else:
            write_log(u"读取请求数据成功")
        for param, value in request_params:
            if param.startswith('#'):
                continue
            query_data.setdefault(param, value)
        if query_data.get('http_req') == "2":
            write_log(u"本次请求是ios发出，需要用https来请求广告")
            self.url = self.url.replace("http", "https")
        query_url = urlencode(query_data)
        self.url = self.url.format(self.host, query_url)

    def get_reponse(self):
        self.build_request_url()
        write_log(u"开始请求广告")
        gr = GetResponse()
        res = ""
        if gr:
            write_log(u"请求成功")
            try:
                res = gr.get_response(self.url)
                self.res = res.json()
                write_log(u"召回信息:\n{0}".format(json.dumps(self.res, indent=4)))
            except Exception:
                write_log(u'请求返回的不是json对象\n\t{0}'.format(res.content),'warn')
        else:
            write_log(u"请求失败!!!", "error")

    def send_url(self):
        pass


def set_res(res_smatto, res_midway):
    # 设置需要比较的字段
    dict_midway = {}
    dict_smatto = {}
    dict_midway.setdefault('title', res_midway.get('data').get('ads')[0].get('title'))
    dict_midway.setdefault('desc', res_midway.get('data').get('ads')[0].get('desc'))
    dict_midway.setdefault('ctatext', res_midway.get('data').get('ads')[0].get('ctatext'))
    dict_midway.setdefault('icon_url', res_midway.get('data').get('ads')[0].get('icon_url'))
    dict_midway.setdefault('image_url', res_midway.get('data').get('ads')[0].get('image_url'))
    dict_midway.setdefault('click_url', res_midway.get('data').get('ads')[0].get('click_url'))
    dict_midway.setdefault('ad_url_list', res_midway.get('data').get('ads')[0].get('ad_url_list'))
    dict_smatto.setdefault('title', res_smatto.get('SNAST').get('adtitle'))
    dict_smatto.setdefault('desc', res_smatto.get('SNAST').get('adtext'))
    dict_smatto.setdefault('ctatext', res_smatto.get('SNAST').get('ctatext'))
    dict_smatto.setdefault('icon_url', res_smatto.get('SNAST').get('iconimage')[0].get('url'))
    dict_smatto.setdefault('image_url', res_smatto.get('SNAST').get('mainimage')[0].get('url'))
    dict_smatto.setdefault('click_url', res_smatto.get('SNAST').get('clickurl'))
    dict_smatto.setdefault('ad_url_list', res_smatto.get('beacons'))
    return dict_smatto, dict_midway


def cmp_res(expect, fact):
    result = True
    cmp_keys = expect.keys()
    for key in cmp_keys:
        expect_value = expect.get(key)
        fact_value = fact.get(key)
        if expect_value != fact_value:
            result = False
            print('{0} is diff:\nexpect: {1}\nfact  : {2}'.format(key, expect_value, fact_value))
            print('-'*20)
    print('='*50)
    return result


def get_res(url_smatto, url_midway ):
    res_smatto = requests.get(url_smatto).json()
    res_midway = requests.get(url_midway).json()
    # 两端都有广告才进行后续比较
    print(url_smatto)
    print(json.dumps(res_smatto, indent=4))
    # print(url_midway)
    # print(json.dumps(res_midway, indent=4))
    # assert res_midway.get('status') == 1
    assert res_smatto.get('status') == "SUCCESS"
    # offerId为七十多亿才是smatto的广告
    # offer_id = res_midway.get('data').get('ads')[0].get("id")
    # assert 7000000000 <= offer_id <= 8000000000
    # dict_smatto, dict_midway = set_res(res_smatto, res_midway)
    # return dict_smatto, dict_midway

def run_demo(sdk_type):
    if sdk_type == "1":
        url_smatto = 'http://soma.smaato.net/oapi/reqAd.jsp?apiver=502&adspace=130320972&pub=1100034804&devip=39.109.124.93&device=Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36&googleadid=ee94a9ba-c079-4786-8867-2ab109ed5610&googlednt=true&androidid=ccf785f98e92d84b&nver=1&format=native&formatstrict=true&response=json&width=1200&height=627'
        # url_midway = "http://test-midway.rayjump.com/openapi/ad/v3?tnum=1&orientation=1&package_name=com.mobvista.sdk.demo&ad_type=42&sign=489942276c3cf759447d81719c104b95&timezone=GMT%252B08%253A00&mnc=&ping_mode=1&platform=1&unit_id=492&os_version=6.0.1&sdk_version=MAL_8.3.0&ttc_ids=%255B%255D&app_version_code=1&req_type=1&brand=google&ad_num=5&app_version_name=1.0&screen_size=1080x1794&mcc=&gp_version=8.1.73.S-all%2520%255B0%255D%2520%255BFP%255D%2520165518514&app_id=24282&offset=0&only_impression=1&ad_source_id=1&gaid=ee94a9ba-c079-4786-8867-2ab109ed5610&dvi=4BzuYk5uRUE0iAVAfURFiah9fnVFfAv0WozwDki0G0RMiUvMiavMiavMiav0WoztYrxBYFQ3%2BFQ3RUE0DFfrfAl2HU39Hn3BHalTD0zK&language=en&is_clever=1&useragent=Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36&model=Nexus%25205X&network_type=9"
    else:
        # url_midway = "https://test-midway.rayjump.com/openapi/ad/v3?tnum=1&orientation=1&package_name=com.tianye1.mvsdk&app_id=22050&ad_source_id=1&country_code=AS&timezone=GMT%252B08%253A00&mnc=&ping_mode=1&category=0&native_info=%255b%257b%2522id%2522%253A2%252C%2522ad_num%2522%253A1%257d%255d&platform=2&unit_id=128&os_version=9.3.5&sdk_version=MI_2.5.0&ttc_ids=%255b%255d&req_type=2&exclude_ids=%255b149653813%255d&http_req=2&idfv=1D710DF9-750C-4923-A4CF-30629D1F9C6B&ad_num=5&app_version_name=2.4.0&screen_size=320.000000x568.000000&mcc=&ad_type=42&display_cids=%255b%28null%29%255d&idfa=35951D6A-DB66-47A1-8CD0-DB1E9E0D33CC&offset=0&only_impression=1&sign=3a7502a2826cf77171f82046b2fdbb44&language=zh-Hans-AS&openidfa=&useragent=Mozilla%252f5.0%2B%28iPhone%25253B%2BCPU%2BiPhone%2BOS%2B9_3_5%2Blike%2BMac%2BOS%2BX%29%2BAppleWebKit%252f601.1.46%2B%28KHTML%25252C%2Blike%2BGecko%29%2BMobile%252f13G36&model=iPhone6%252C2&network_type=2"
        url_smatto = "https://soma.smaato.net/oapi/reqAd.jsp?apiver=502&adspace=130320969&pub=1100034804&devip=39.109.124.93&device=Mozilla%252f5.0%2B%28iPhone%25253B%2BCPU%2BiPhone%2BOS%2B9_3_5%2Blike%2BMac%2BOS%2BX%29%2BAppleWebKit%252f601.1.46%2B%28KHTML%25252C%2Blike%2BGecko%29%2BMobile%252f13G36&iosadid=35951D6A-DB66-47A1-8CD0-DB1E9E0D33CC&iosadtracking=true&nver=1&format=native&formatstrict=true&response=json&width=1200&height=627"
    # res_smatto, res_midway = get_res(url_smatto, url_midway)
    res = requests.get(url_smatto)
    print(json.dumps(res.json(), indent=4))
    print('='*50)
    print('cmp result as below:')
    # cmp_res(res_smatto, res_midway)
    print('+'*100)


if __name__ == "__main__":
    while True:
        sdk_type = raw_input('choose sdk, 1-andriod|2-ios: ')
        run_demo(sdk_type)
