import requests
import json

dict_num = {'ios_all': 0, 'ios_click': 0, 'android_all': 0, 'android_click': 0}


def get_inmobi_res(req_type):
    global dict_num
    url = "http://api.uniplayad.com/phone/agent.php"
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

    body_android = {
	    "app": {
	        "an": "AppStore",
	        "pkg": "com.wz.demo",
	        "ver": "1.0.2_20160328",
	        "vc": 102,
	        "ist": "1459178160116"
	    },
	    "device": {
	        "icc": "460030911072565",
	        "ime": "A1000037D0DF28",
	        "mac": "02:00:00:00:00:00",
	        "plt": 1,
	        "ov": "6.0",
	        "dpi": "2.0",
	        "swidth": "720",
	        "sheight": "1080",
	        "mdl": "HTC D816d",
	        "brd": "HTC",
	        "aid": "1040003666478",
	        "lg": "zh",
	        "net": 3,
	        "opt": "46003",
	        "pn": "18910893960",
	        "si": 1,
	        "ssid": "DONOPO-AP9",
	        "bssid": "e4:f4:c6:06:be:27",
	        "ua": "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9sk Build/MMB29M; wv)AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 MobileSafari/537.36"
	    },
	    "geo": {
	        "lgd": "32.232",
	        "ltd": "116.63",
	        "addr": 'beijing'
	    },
	    "adw": 320,
	    "adh": 50,
	    "appid": "1712120004",
	    "slotid": "video",
	    "ip": "175.25.188.3"
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




