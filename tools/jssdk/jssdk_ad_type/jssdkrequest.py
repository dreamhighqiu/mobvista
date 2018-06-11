# -*- coding: utf-8 -*-
'''
Created on ：2018/6/5:15:39

@author: yunxia.qiu
'''

from utils.http_req import  Request
from format_url import params2dict
class jssdk_request():

    def __init__(self,url):
        self.ANDROID_UA = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36"}
        self.IOS_UA = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"}

        self.new_url, self.params = params2dict(url)

        self.r=Request(self.new_url,params=self.params)
    def change_params(self):

        print(self.params['platform'])

        if self.params['platform']==str(2):
            self.params['useragent']= self.IOS_UA['User-Agent']
            self.params['model']='iphone10.3'
        else:
            self.params['useragent'] = self.ANDROID_UA['User-Agent']
            self.params['model'] = 'android4.4'

    def send_req(self):
        #self.change_params()
        self.r = Request(self.new_url, params=self.params)
        res=self.r.send_request()
        #print(res)
        body=res.get('body')



if __name__=='__main__':
    url1='http://net.rayjump.com/openapi/jssdkad?only_impression=1&app_id=31609&unit_id=34768&ping_mode=1&sign=105d93d991325adfeaf15ed641bdf8f7&content_type=286&network_type=9&main_domain=pingan.i99pay.com&screen_size=980x1461&platform=2&orientation=1&useragent=Mozilla/5.0%20(iPhone;%20CPU%20iPhone%20OS%209_1%20like%20Mac%20OS%20X)%20AppleWebKit/601.1.46%20(KHTML,%20like%20Gecko)%20Version/7.0%20Mobile/13B143%20Safari/9537.53&ad_num=1&offset=1&os_version=9.1&sdk_version=js_1.1.10&image_size=7&android_id=&imei=&gaid=&http_req=2&model=iphone9,1&deviceid=&language=zh-cn&version_flag=1&api_version=1.1&exclude_ids=[183455318,191002764,202573155,210434850]&tnum=1&ttc_ids=[]&client_ip=null&ts=1528250060435'
    url='https://net.rayjump.com/openapi/jssdkad?only_impression=1&app_id=31609&unit_id=31327&ping_mode=1&sign=105d93d991325adfeaf15ed641bdf8f7&content_type=94&network_type=4&main_domain=pingan.i99pay.com&screen_size=980x1743&platform=2&orientation=1&useragent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"&ad_num=1&offset=3&os_version=11.0&sdk_version=js_1.1.10&image_size=7&android_id=&imei=&gaid=&http_req=2&model=iphone10,3&deviceid=&language=zh-CN&version_flag=1&api_version=1.1&exclude_ids=[]&tnum=1&ttc_ids=[]&client_ip=null&ts=1528095525572'
    r=jssdk_request(url)
    r.send_req()
