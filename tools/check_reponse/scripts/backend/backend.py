# encoding:utf-8
import json

import requests

from check_reponse.config import BACKEND_CONFIG
from check_reponse.scripts.common.cmp_utils import cmp_dict_data_pass_diff
from check_reponse.scripts.common.file_utils import write_log, read_file
from check_reponse.scripts.common.request_utils import GetResponse


class AdBackend(GetResponse):
    def __init__(self, interface_type="v3", backend_id=0):
        GetResponse.__init__(self)
        self.rs = requests.session()
        backend_config = BACKEND_CONFIG.get(interface_type).get(int(backend_id))
        self.backend_name = backend_config.get("name")
        self.backend_host = backend_config.get("host")
        self.backend_url = backend_config.get("url")
        self.backend_method = backend_config.get("method")
        self.backend_headers = backend_config.get("headers")
        self.backend_request_data_type = backend_config.get("request_data_type")
        self.backend_request_data_path = backend_config.get("request_data_path")
        self.backend_response_data_type = backend_config.get("response_data_type")
        self.backend_response_data_path = backend_config.get("response_data_path")
        self.backend_set_pass = backend_config.get("set_pass")
        self.query_data = {}
        self.response = None
        self.url_list = []

    def set_request_info(self, file_index):
        self.backend_request_data_path = self.backend_request_data_path.format(file_index)
        self.backend_response_data_path = self.backend_response_data_path.format(file_index)
        write_log("request data path: {0}".format(self.backend_request_data_path))
        write_log("request host: {0}".format(self.backend_host))
        write_log("request method: {0}".format(self.backend_method))
        self.backend_url = self.backend_url.format(self.backend_host)
        write_log("request route: {0}".format(self.backend_url))
        self.query_data = read_file(self.backend_request_data_type, "dict", self.backend_request_data_path)
        # if self.query_data:
        #     if self.query_data.get('http_req') == "2":
        #         write_log("for ios request ,use https")
        #         self.backend_url = self.backend_url.replace("http://", "https://")

    def get_my_response(self, file_index):
        self.set_request_info(file_index)
        self.get_response(self.backend_url, self.backend_method, self.backend_headers, self.query_data)
        if self.res:
            if self.backend_response_data_type == "json":
                self.response = self.res.json()
                write_log("response is: {0}".format(json.dumps(self.response, indent=4)))
            else:
                self.response = self.res.content
                write_log("response is: {0}".format(self.response))
        else:
            write_log("request failed, no response to check", 'error')
            raise ValueError

    def check_my_response(self, file_index, check=False, set_pass=None):
        self.url_list = []
        self.get_my_response(file_index)
        if check:
            if self.backend_response_data_type == "json":
                expect_response = read_file(self.backend_response_data_type, "json", self.backend_response_data_path)
            else:
                expect_response = read_file(self.backend_response_data_type, "str", self.backend_response_data_path)
            cmp_dict_data_pass_diff(expect_response, self.response, set_pass=self.backend_set_pass)

    def find_all_urls(self, data, condition=".startswith('http')"):
        if not isinstance(data, (list, dict)):
            return self.url_list
        if isinstance(data, dict):
            data = data.values()
        for i in data:
            if isinstance(i, (list, dict)):
                self.find_all_urls(i, condition)
            elif isinstance(i, (str, unicode)):
                if not condition or (condition and eval('i'+condition)):
                    i = i.replace("https://", "http://")
                    self.url_list.append(i)
                    # 需要组装install_url
                    if i.find('/click?k=') >= 0:
                        if len(i.split('q=')) > 1:
                            conversion_url = "http://{0}/conversion?from=mobilecore&click_id={1}&notice=1"\
                                .format(self.backend_host.replace("midway", "net"), i.split('q=')[1].split('&')[0])
                            self.url_list.append(conversion_url)

    def send_tracking(self, tracking_data, set_domain=set()):
        # 只发送第一个campaign的tracking信息
        self.find_all_urls(tracking_data)
        if not self.url_list:
            write_log('no url to send!', 'warn')
            return
        write_log('send url in response, summary: {0}'.format(len(self.url_list)))
        for url in self.url_list:
            try:
                for domain in set_domain:
                    # 只发送指定domain的请求
                    if url.find(domain) in [7, 8]:
                        self.get_response(url)
            except StandardError:
                write_log('send url failed \n %s!!!' % url, 'error')

