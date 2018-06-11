# encoding:utf-8
import requests
import json
import urllib
from file_utils import write_log


class GetResponse:
    def __init__(self):
        self.rs = requests.session()
        self.res = None

    def get_response(self, request_url, method="GET", headers={}, data={}, ex_code=200):
        # write_log(u"请求的method: {0}".format(method))
        # if headers:
        #     write_log(u"请求的headers: {0}".format(headers))
        # if data:
        #     write_log(u"请求的data: {0}".format(data))
        try:
            if method.upper() == 'POST':
                if headers.get('Content-type') == "application/json":
                    data = json.dumps(data)
                write_log(u"请求的url: {0}".format(request_url))
                self.res = requests.post(request_url, headers=headers, data=data, timeout=1)
            else:
                request_url += urllib.urlencode(data)
                write_log(u"请求的url: {0}".format(request_url))
                self.res = requests.get(request_url, headers=headers, timeout=10)
            if self.res.status_code != ex_code:
                write_log(u'返回的状态码错误，预期是：{0}，实际是：{1}'.format(ex_code, self.res.status_code), 'error')
        except Exception as e:
            write_log(u"请求失败，原因：{0}".format(e), 'error')
        return self.res

    def check_response(self):
        pass

if __name__ == "__main__":
    gr = GetResponse()
    # url = "http://test-net.rayjump.com/openapi/ads?tnum=5&orientation=1&package_name=com.tianye1.mvsdk&app_id=22050&ad_source_id=1&country_code=AS&timezone=GMT%25252B08%25253A00&mnc=&ping_mode=1&category=0&platform=2&unit_id=607&os_version=9.3.5&sdk_version=MI_2.4.0&ttc_ids=%25255b%25255d&req_type=3&exclude_ids=%25255b149653813%25255d&http_req=2&client_ip=42.199.59.153&idfv=1D710DF9-750C-4923-A4CF-30629D1F9C6B&ad_num=5&app_version_name=2.4.0&screen_size=320.000000x568.000000&mcc=&ad_type=94&display_cids=%25255b133783406%25255d&idfa=35951D6A-DB66-47A1-8CD0-DB1E9E0D33CC&offset=1&only_impression=1&sign=3a7502a2826cf77171f82046b2fdbb44&language=zh-Hans-AS&version_flag=1&session_id=5966d893ac0f4e5e1c48b5f6&openidfa=&useragent=Mozilla%25252f5.0%252B%2528iPhone%2525253B%252BCPU%252BiPhone%252BOS%252B9_3_5%252Blike%252BMac%252BOS%252BX%2529%252BAppleWebKit%25252f601.1.46%252B%2528KHTML%2525252C%252Blike%252BGecko%2529%252BMobile%25252f13G36&model=iPhone6%25252C2&network_type=2"
    url = "https://test-net.rayjump.com/openapi/ads?tnum=5&orientation=1&package_name=1001548937&app_id=32706&ad_source_id=1&country_code=AS&timezone=GMT%252B08%253A00&mnc=&ping_mode=1&category=0&native_info=%255b%257b%2522id%2522%253A2%252C%2522ad_num%2522%253A1%257d%255d&platform=2&unit_id=6076&os_version=9.3.5&sdk_version=MI_2.5.1&ttc_ids=%255b%255d&req_type=2&exclude_ids=%255b149653813%255d&http_req=2&client_ip=42.199.59.153&idfv=1D710DF9-750C-4923-A4CF-30629D1F9C6B&ad_num=10&app_version_name=2.4.0&screen_size=320.000000x568.000000&mcc=&ad_type=42&display_cids=%255b%28null%29%255d&idfa=35951D6A-DB66-47A1-8CD0-DB1E9E0D33CC&offset=0&only_impression=1&sign=f9036fd79119bc9fc3bd5929370122ea&language=zh-Hans-AS&openidfa=&useragent=Mozilla%252f5.0%2B%28iPhone%25253B%2BCPU%2BiPhone%2BOS%2B9_3_5%2Blike%2BMac%2BOS%2BX%29%2BAppleWebKit%252f601.1.46%2B%28KHTML%25252C%2Blike%2BGecko%29%2BMobile%252f13G36&model=iPhone6%252C2&network_type=2"
    res = gr.get_response(url, 'GET', {}, {}).json()
    # print(json.dumps(res, indent=4))
    ads = res.get('data').get('ads')
    for ad in ads:
        if ad.get('ttc'):
            print(json.dumps(ad, indent=4))
        # print(json.dumps(ad, indent=4))