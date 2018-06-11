#coding=UTF-8
import requests
import json
sum_num=0
count=10
dict_camp = {}
url='https://net.rayjump.com/openapi/jssdkad?only_impression=1&app_id=31609&unit_id=31327&ping_mode=1&sign' \
    '=105d93d991325adfeaf15ed641bdf8f7&content_type=94&network_type=9&main_domain=pingan.i99pay.com&screen_size' \
    '=980x1461&platform=2&orientation=1&useragent=Mozilla/5.0%20(' \
    'iPhone;%20CPU%20iPhone%20OS%209_1%20like%20Mac%20OS%20X)%20AppleWebKit/601.1.46%20(KHTML,' \
    '%20like%20Gecko)%20Version/7.0%20Mobile/13B143%20Safari/9537.53&ad_num=1&offset=3&os_version=9.1&sdk_version' \
    '=js_1.1.10&image_size=7&android_id=&imei=&gaid=&http_req=2&model=iphone9,' \
    '1&deviceid=&language=zh-cn&version_flag=1&api_version=1.1&exclude_ids=[]&tnum=1&ttc_ids=[' \
    ']&client_ip=null&ts=1528252038319'



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
