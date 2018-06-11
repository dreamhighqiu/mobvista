#coding=UTF-8
import requests
import json
sum_num=0
count=50
dict_camp = {}
url="http://se.rayjump.com/openapi/ads?ad_num=1&app_id=102155&brand=&category=2&client_ip=124.207.212.130&idfa=C37641B1-EAA7-485A-A312-95B6ECE2C1D5&idfv=A1F5BEB2-B802-4718-AF9F-EAB525F116FF&image_size=6&model=&network_type=9&os_version=11.3&package_name=com.douban.frodo&platform=2&sign=fc0ab0340b84ffe4a55f1a6cce6a9d48&unit_id=37113&useragent=api-client%2F0.1.3+com.douban.frodo%2F5.25.1+iOS%2F11.3+iPhone7%2C2+network%2Fwifi%20HTTP/1.1%22%20200%201983%20%22-%22%20%22api-client/" \
    "0.1.3%20com.douban.frodo/5.25.1%20iOS/11.3"



for i in range(count):
    try:
        res = requests.get(url)
        res_json = res.json()
        if res_json.get("status") == 1:
            sum_num+=1
            list_camp = res_json.get("data").get("ads")
            for camp in list_camp:
                camp_id = camp.get("id")
                camp_name = camp.get("title")
                # if camp_id not in dict_camp:
                #     dict_camp[camp_id] = camp_name
                #     print(u"广告id:%d,广告title:%s"%(camp_id, camp_name))
                dict_camp[camp_id] = camp_name
                print(u"广告id为%d,广告title为%s"%(camp_id, camp_name))
    except StandardError:
        continue

print(json.dumps(dict_camp).decode("unicode_escape").encode("utf-8"))
print(",".join([str(_) for _ in dict_camp.keys()]))
print(u"总共刷%d次接口，刷到offer为%s"%(count,sum_num))
