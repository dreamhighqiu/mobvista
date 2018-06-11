import requests
import json

dict_num = {'ios_all': 0, 'ios_click': 0, 'android_all': 0, 'android_click': 0}


def get_inmobi_res(req_type):
    global dict_num
    url = "http://api.w.inmobi.com/showad/v3.1"
    # zw 1507405043238 1507919834219
    # test 1496162568792
    body_ios = {
        "imp": {
            "native": {"layout": 2, "screenWidth": 414},
            "secure": 1,
            "trackertype": "url_ping",
            "ext": {"ads": 1}
        },
        "app": {"bundle": "com.lenovo.anyshare", "id": "1507919834219"},
        "device": {"ifa": "E8075B90-D5D7-43F5-B473-12C5C6FDB872",
                   "ua": "Mozilla/5.0%20%28iPhone%3B%20CPU%20iPhone%20OS%2010_3_3%20like%20Mac%20OS%20X%29%20AppleWebKit/603.3.8%20%28KHTML%2C%20like%20Gecko%29%20Mobile/14G60ike+Gecko)+Mobile%2f13G36",
                   "ip": "61.0.50.12"
                   },
        "ext": {"responseformat": "json"}
    }

    # body_ios = {
    #     "device": {
    #         "ip": "61.0.50.12",
    #         "ua": "Mozilla/5.0 (Linux; Android 5.1; XT1033 Build/LPB23.13-56; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.105 Mobile Safari/537.36",
    #         "gpid": "6b6a651d-74d4-4ccb-bbe6-ac561db382cc"
    #     },
    #     "imp": {
    #         "ext": {
    #             "ads": 1
    #         },
    #         "trackertype": "url_ping",
    #         "secure": 1,
    #         "native": {
    #             "screenWidth": 414,
    #             "layout": 2
    #         }
    #     },
    #     "app": {
    #         "id": "1507405043238",
    #         "bundle": "vStudio.Android.Camera360"
    #     },
    #     "ext": {
    #         "responseformat": "json"
    #     }
    # }

    body_android = {
        "imp": {
            "native": {"layout": 2, "screenWidth": 1080},
            "secure": 0,
            "trackertype": "url_ping",
            "ext": {"ads": 1}
        },
        "app": {"bundle": "com.mobvista.sdk.demo", "id": "1495284125502"},
        # zw 1495284125502
        # cs 1494247743956
        "device": {
            "gpid": "5e37de58-0d9f-4bb2-8d8a-5a2200240614",     # ee94a9ba-c079-4786-8867-2ab109ed5610  5e37de58-0d9f-4bb2-8d8a-5a2200240614
            "ip": "61.0.50.12",  # 61.0.50.0  hk-39.109.124.93 us-54.88.166.80 112.94.162.245
            "ua": "Mozilla/5.0 (Linux; Android 5.0.2; SM-G530H Build/LRX22G) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"
        },
        "ext": {"responseformat": "json"}
    }
    # body_android = {"imp":{"native":{"layout":2,"screenWidth":1080},"secure":0,"trackertype":"url_ping","ext":{"ads":1}},"app":{"bundle":"com.mobvista.sdk.demo","id":"1507405043238"},"device":{"gpid":"5e37de58-0d9f-4bb2-8d8a-5a2200240614","ip":"39.109.124.93","ua":"Mozilla/5.0 (Linux; Android 5.0.2; SM-G530H Build/LRX22G) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"},"ext":{"responseformat":"json"}}
    header = {"Content-Type": "application/json"}
    body = body_android
    if req_type != 1:
        body = body_ios
        url = url.replace('http', 'https')
    # print(json.dumps(body, indent=4))
    res = requests.post(url=url, data=json.dumps(body), headers=header)
    try:
        res = res.json()
        print(json.dumps(res, indent=4, sort_keys=False, ensure_ascii=False))
        return res
    except StandardError:
        print("error status_code %s"%res.status_code)

    # for offer in res.get('ads'):
    #     click_urls = offer.get('eventTracking').get('8').get('urls')
    #     if req_type == 1:
    #         dict_num['ios_all'] += 1
    #         click_url = click_urls[0]
    #         print(click_url)
    #         if click_url.find('c.w.inmobi.com') > 0:
    #             dict_num['ios_click'] += 1
    #     else:
    #         dict_num['android_all'] += 1
    #         click_url = click_urls[1]
    #         print(click_url)
    #         if click_url.find('c.w.inmobi.com') > 0:
    #             dict_num['android_click'] += 1


if __name__ == '__main__':
    # 1-ios 2-android
    while True:
        sdk_type = raw_input('choose sdk, 1-android|2-ios: ').strip()
        for i in range(1):
            if sdk_type == "1":
                get_inmobi_res(1)
            else:
                get_inmobi_res(2)
            print("this is round %s"%i)
            print('-'*20)
        print('='*20)
