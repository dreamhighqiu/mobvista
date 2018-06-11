# encoding:utf-8
"""
MV召回接口
"""

from urllib import urlencode
from check_reponse.scripts.common.file_utils import read_csv_to_list, write_log
from check_reponse.scripts.common.request_utils import GetResponse
import json


class Mobvista:
    def __init__(self, host="test-net.rayjump.com", file_index="1"):
        self.url = "http://{0}/openapi/ad/v3?{1}"
        self.host = host
        self.data_path = "../../data/mobvista/"
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
            # self.url = self.url.replace("http://", "https://")
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
                write_log(u'请求返回的不是json对象\n\t{0}'.format(res),'warn')
        else:
            write_log(u"请求失败!!!", "error")

    def send_url(self):
        pass

    def check_response(self):
        pass


if __name__ == "__main__":
    platform = "1"      # 1-android|2-ios
    ad_format = "94"    # 42-native|94-reward_video
    content = "3"       # 2-image|3-video
    file_index = "{0}_{1}_{2}".format(platform, ad_format, content)
    mv = Mobvista(host="test-midway.rayjump.com", file_index=file_index)
    list_tempid = []
    for i in range(1):
        mv.get_reponse()
        tempid = mv.res.get('data').get('ads')[0].get("rv").get("video_template")
        list_tempid.append(tempid)
    print(set(list_tempid))





