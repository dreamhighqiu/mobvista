# coding=UTF-8

import json
import keyword
print(dir(keyword))

dict_camp = {}
from format_url import params2dict
import requests
class camp_data():
    def __init__(self,url,count=0,sum=0):
        self.new_url, self.params = params2dict(url)
        #print(self.new_url,self.params)
        self.sum_num=sum
        self.count=count

    def req_data(self,platform_type):
        for i in range(self.count):
            try:
                print(u'*******************第%d个请求********************************'%(i+1))
                self.ANDROID_UA = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36"}
                self.IOS_UA = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"}
                #公共修改params部分，修改请求

                if platform_type=='ios':
                    self.params['useragent'] = self.IOS_UA['User-Agent']
                    self.params['model'] = 'iphone10.3'
                    self.params['os_version']=10.3
                    self.params['platform']=str(2)

                else:
                    self.params['useragent'] = self.ANDROID_UA['User-Agent']
                    self.params['model'] = 'android4.4'
                    self.params['os_version'] = 4.4
                    self.params['platform'] = str(1)


                self.params['offset']=i
                res = requests.get(self.new_url,params=self.params,verify=False)
                res_json = res.json()

                #print(res.url)
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



if __name__=='__main__':
    url = "https://net.rayjump.com/openapi/jssdkad?only_impression=1&app_id=102641&unit_id=38527&ping_mode=1&sign" \
          "=0823a6534adb3e69f24b6f5a8137f319&content_type=285&network_type=9&main_domain=www.meipian.cn&screen_size" \
          "=343x150&platform=2&orientation=2&useragent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) " \
          "AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1&ad_num=1&offset=0&os_version=10.3&sdk_version=js_1.1.10&image_size=7&android_id=&imei=&gaid=&http_req=2&model=iphone10,3&deviceid=&language=zh-CN&version_flag=1&api_version=1.1&exclude_ids=[]&tnum=1&ttc_ids=[]&client_ip=null&ts=1528276870492"
    r=camp_data(url,2)
    r.req_data('android')


