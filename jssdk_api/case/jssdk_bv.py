# -*- coding: utf-8 -*-
'''
Created on ：2018/6/7:11:22

@author: yunxia.qiu
'''
from jssdk_api.util.format_url import params2dict
import time
from config.ParseConfigurationFile import ParseConfigfile
import requests
import json

class jssdk_banner_video():

    def __init__(self,count=0):
        self.count=count
        self.sum_num=0
        p = ParseConfigfile()
        self.url = p.getOptionValue('url', 'bv_url')
        self.new_url,self.params=params2dict(self.url)
        self.app_id=p.getOptionValue('banner_video','app_id')
        self.unit_id=p.getOptionValue('banner_video', 'unit_id')
        self.sign=p.getOptionValue('banner_video', 'sign')
        self.content_type=p.getOptionValue('banner_video','content_type')
        self.platform = p.getOptionValue('common', 'platform')
        self.ANDROID_UA = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36"}
        self.IOS_UA = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"}
        # 公共修改params部分，修改请求


    def change_params(self):

        self.params['content_type']=self.content_type
        self.params['app_id']=self.app_id
        self.params['unit_id']=self.unit_id
        self.params['sign']=self.sign
        self.params['platform'] = self.platform
        self.params['ts']=time.time()

        if self.params['platform'] == str(2):

            self.params['useragent'] = self.IOS_UA['User-Agent']
            self.params['model'] = 'iphone10.3'
            self.params['os_version'] = 10.3
            self.params['platform'] = str(2)

        else:
            self.params['useragent'] = self.ANDROID_UA['User-Agent']
            self.params['model'] = 'android4.4'
            self.params['os_version'] = 4.4
            self.params['platform'] = str(1)
    def common_params(self):
        self.params['orientation']=1
        self.params['offset']=100
        self.params['platform']=2
        self.params['network_type']=4
        self.params['client_ip']='null'
        self.params['language']='zh-CN'
        self.params['deviceid']=""
        self.params['imei']=""
        self.params['gaid'] = ""
        self.params['version_flag'] = ""
        self.params['exclude_ids'] = []
        self.params['api_version'] = []
        self.params['os_version'] = ""
        self.params['sdk_version'] = ""
        self.params['http_req'] = 2
        self.params['ad_num'] = ""




    def req_data(self):
        dict_camp={}
        for i in range(self.count):
            try:
                print(u'*******************第%d个请求********************************'%(i+1))
                self.params['offset']=i
                res = requests.get(self.new_url,params=self.params,verify=False)
                res_json = res.json()

                print(res.url)
                #print(json.dumps(res_json,ensure_ascii=False,indent=4))

                #获取响应数据
                if res_json.get("status") == 1:
                    list_camp = res_json.get("data").get("ads")
                    self.sum_num += 1
                    #print(json.dumps())
                    for camp in list_camp:
                        camp_id = camp.get("id")
                        camp_name = camp.get("title")
                        dict_camp[camp_id] = camp_name
                        print("%s %s" % (camp_id, camp_name))
                else:
                    print(res_json)

            except StandardError:
                continue

        print(json.dumps(dict_camp,ensure_ascii=False,indent=4))
        print(",".join([str(_) for _ in dict_camp.keys()]))
        print(u"总共刷%d次接口，刷到offer为%s" % (self.count, self.sum_num))




if __name__=="__main__":

    bv=jssdk_banner_video(10)
    bv.change_params()
    bv.req_data()





