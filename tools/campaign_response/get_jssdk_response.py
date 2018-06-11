# coding=UTF-8
import requests
import json


dict_camp = {}
sum_num =0
count=1
url = "https://net.rayjump.com/openapi/jssdkad?only_impression=1&app_id=31609&unit_id=31327&ping_mode=1&sign=105d93d991325adfeaf15ed641bdf8f7&content_type=94&network_type=9&main_domain=pingan.i99pay.com&screen_size=980x1430&platform=1&orientation=1&useragent=Mozilla/5.0%20(Linux;%20U;%20Android%205.1;%20zh-CN;%20OPPO%20A37m%20Build/LMY47I)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Version/4.0%20Chrome/57.0.2987.108%20UCBrowser/11.9.8.978%20Mobile%20Safari/537.36&ad_num=1&offset=2&os_version=5.1&sdk_version=js_1.1.9&image_size=7&android_id=&imei=&gaid=&http_req=2&model=android%20phone&deviceid=&language=zh-CN&version_flag=1&api_version=1.1&exclude_ids=[]&tnum=1&ttc_ids=[]&client_ip=null&ts=1527246184906"


for i in range(count):
    try:
        res = requests.get(url,verify=False)
        res_json = res.json()

        if res_json.get("status") == 1:
            list_camp = res_json.get("data").get("ads")
            sum_num += 1
            setting = res_json.get("data").get('setting')
            print(json.dumps(setting,ensure_ascii=True,indent=4,sort_keys=True))
            # print(json.dump(setting))
            for camp in list_camp:
                camp_id = camp.get("id")
                camp_name = camp.get("title")
                dict_camp[camp_id] = camp_name
                print("%s %s" %(camp_id, camp_name))
    except StandardError:
        continue

print(json.dumps(dict_camp).decode("unicode_escape").encode("utf-8"))
print(",".join([str(_) for _ in dict_camp.keys()]))
print(u"总共刷%d次接口，刷到offer为%s"%(count,sum_num))
