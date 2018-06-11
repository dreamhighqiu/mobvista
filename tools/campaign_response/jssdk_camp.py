# coding=UTF-8
import requests
import json



dict_camp = {}
sum_num =0
count=5
url ="https://net.rayjump.com/openapi/jssdkad?only_impression=1&app_id=31609&unit_id=34769&ping_mode=1&sign=105d93d991325adfeaf15ed641bdf8f7&content_type=285&network_type=9&main_domain=pingan.i99pay.com&screen_size=980x1892&platform=2&orientation=1&useragent=Mozilla/5.0%20(iPhone;%20CPU%20iPhone%20OS%2011_3%20like%20Mac%20OS%20X)%20AppleWebKit/605.1.15%20(KHTML,%20like%20Gecko)%20Mobile/15E216%20MicroMessenger/6.6.6%20NetType/WIFI%20Language/zh_CN&ad_num=1&offset=3&os_version=11.3&sdk_version=js_1.1.10&image_size=7&android_id=&imei=&gaid=&http_req=2&model=iphone11,3&deviceid=&language=zh-CN&version_flag=1&api_version=1.1&exclude_ids=[]&tnum=1&ttc_ids=[]&client_ip=218.19.46.219&ts=1528256427369"


for i in range(count):
    try:
        res = requests.get(url,verify=False)
        res_json = res.json()

        if res_json.get("status") == 1:
            list_camp = res_json.get("data").get("ads")
            sum_num += 1
            for camp in list_camp:
                camp_id = camp.get("id")
                camp_name = camp.get("title")
                dict_camp[camp_id] = camp_name
                print("%s %s" %(camp_id, camp_name))
    except StandardError:
        continue

print(json.dumps(dict_camp).decode("unicode_escape").encode("utf-8"))
#print(json.dumps(dict_camp,ensure_ascii=True,indent=4).decode("utf-8").encode("utf-8"))
print(",".join([str(_) for _ in dict_camp.keys()]))
print(u"总共刷%d次接口，刷到offer为%s"%(count,sum_num))
