# -*- coding: utf-8 -*-
'''
Created on ：2018/6/5:15:11

@author: yunxia.qiu
'''
import re
import json

url='https://net.rayjump.com/openapi/jssdkad?only_impression=1&app_id=31609&unit_id=31327&ping_mode=1&sign=105d93d991325adfeaf15ed641bdf8f7&content_type=94&network_type=4&main_domain=pingan.i99pay.com&screen_size=980x1743&platform=2&orientation=1&useragent=Mozilla/5.0%20(iPhone;%20CPU%20iPhone%20OS%2011_0%20like%20Mac%20OS%20X)%20AppleWebKit/604.1.38%20(KHTML,%20like%20Gecko)%20Version/11.0%20Mobile/15A372%20Safari/604.1&ad_num=1&offset=3&os_version=11.0&sdk_version=js_1.1.10&image_size=7&android_id=&imei=&gaid=&http_req=2&model=iphone11,0&deviceid=&language=zh-CN&version_flag=1&api_version=1.1&exclude_ids=[]&tnum=1&ttc_ids=[]&client_ip=null&ts=1528095525572'
def params2dict(url):
    url, params = re.split(r'[?]', url)
    data = re.split('&', params)
    # print(data)
    # print(str(data))
    k = []
    v = []
    for i in data:
        k.append(re.split('=', i)[0])
        v.append(re.split('=', i)[1])
    dict_data = dict(zip(k, v))
    #data = json.dumps(dict_data)
    #print(url,dict_data)

    return url,dict_data
params2dict(url)
