# encoding:utf-8
"""
雷霆召回接口
"""

from urllib import urlencode
from check_reponse.scripts.common.file_utils import read_csv_to_list, write_log
from check_reponse.scripts.common.request_utils import GetResponse
import json

# url = "https://logmonitor.leiting.com/mobvistaNativeWd?client_ip=39.109.124.93&ua=%7B%7BuserAgent%7D%7D&os=ios&idfa=BFDC503D-EBCD-4876-B1E7-41299FAE8703&osv=10.3.3&deal_id=59ef4090c6c1e23ce2000002&unit_id=128"

class Leiting:
    def __init__(self, host="logmonitor.leiting.com", file_index="1"):
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

if __name__ == "__main__":
    Leiting(file_index="2_42_2").get_reponse()



