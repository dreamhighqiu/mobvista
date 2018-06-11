import requests
import json
import random
import string



url = "https://is.snssdk.com/api/ad/union/get_ads_json"

body_ios = {
    "request_id": ''.join(random.sample(string.ascii_letters + string.digits, 32)),
    "api_version": "1.6",
    "uid": "",
    "source_type": "app",
    "ua": "Mozilla/5.0%20(iPhone%3B%20CPU%20iPhone%20OS%2010_2_1%20like%20Mac%20OS%20X)%20AppleWebKit/602.4.6%20(KHTML%2C%20like%20Gecko)%20Mobile/14D27%20Camera360/8.3.4",
    "ip": "219.137.150.254",
    "app": {
        "appid": "5001083"
    },
    "device": {
        "did": "C98B99BB-1B2F-434E-BE53-FD651B03FB6A",
        "imei": "",
        "type": 1,
        "os": 2,
        "os_version": "10.3.1",
        "vendor": "0",
        "model": "iPhone8,1",
        "language": "en-JP",
        "conn_type": 1,
        "mac": "",
        "screen_width": 375,
        "screen_height": 667
    },
    "adslots": [
        {
            "id": "901083128",
            "adtype": 7,
            "pos": 5,
            "accepted_size": [
                {
                    "width": 1200,
                    "height": 627
                }
            ],
            "ad_count": 1
        }
    ]
}

body_android = {
    "request_id": ''.join(random.sample(string.ascii_letters + string.digits, 32)),
    "api_version": "1.6",
    "uid": "",
    "source_type": "app",
    "ua": "Mozilla%2F5.0%20%28Linux%3B%20Android%206.0.1%3B%20Nexus%205X%20Build%2FMTC19T%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F60.0.3112.116%20Mobile%20Safari%2F537.36",
    "ip": "112.94.162.245",
    "app": {
        "appid": "5001293"
    },
    "device": {
        "did": "",
        "imei": "35362607855670",
        "android_id": "ccf785f98e92d84b",
        "type": 1,
        "os": 1,
        "os_version": "5.0.1",
        "vendor": "google",
        "model": "Nexus%205X",
        "language": "en",
        "conn_type": 1,
        "mac": "020000000000",
        "screen_width": 540,
        "screen_height": 960
    },
    "adslots": [
        {
            "id": "901293829",
            "adtype": 7,
            "pos": 5,
            "accepted_size": [
                {
                    "width": 1200,
                    "height": 627
                }
            ],
            "ad_count": 1
        }
    ]
}

"""
url_track = "https://is.snssdk.com/api/ad/union/event_report/"
body_track = {"event_type": 1, "extra":"yIUTvltu5dX4OY2yZDZk44Lr6JOX%2BnKTzabPmT3jh0gLX5EIlbBQzxLP185ApiV3OgIW180whKtO2WJSI6bIKC%2FdD4LsW9%2F%2F%2BeKZXQHy6N50i8Dea34hoiGqk8qO%2FicmFki3TvoEGAP3pTcwSRuwkX5ykr8JYYMJuBRhTX19vdvWIA%2BI8xDSDo3jBb8rhOYFWnmyr6yroF0bqKukKOHP1QbydNsV2NRBfWQ40HS23HEglTiB3VUPudHyFMApH5V7AAXIDqAJOy0OXCY7VhpBvFthoP2Ll6wJbYdNIau7l3jQ2Yk29jtIGyWAKjDFQD9HT%2BZeFMXGYTxBLjKsu8rlVvaWvHbdXxtrxWw2Vnlxy6v8C4y7QBkB0ePoj%2BrCa8%2BhgXnmvvJ%2FlApVuSJawGU8fIMRF4HHTQC272rRolPvJjMfQEoURB0opd3hm1GpBWH2LI1Ts7KmJ0VsWXvsyLv9V6zQj8%2Fbc2pzYnCWZ75B4z4vpWPZQONfst%2FLa%2BHS%2FVcMH%2FI6DujkkMPB%2BAs0r2eJH6sM9Hx6AP23vidPsRJQChTP%2Bn3tEGbWrwyqjTb326%2FCYRSRb8DuV5GZroit0TGQD2%2BvV0Gb2JDoZJNyYvCEF2SIYXGveLhuZVLjooUTszCvbyqmIFXtjYPC%2BfhDFMIwLjsDpxKqThubFSyul%2BKKstF%2F1Lqr3zJUGg1QtJ9Lum%2BzTkJhkWCODntcpHXlhtF9Rt%2BKaFDQuFt2yjLq3Ysdi3EDVqFhPWPZVV4cCntJOvR%2BxiOsM2mYIPIhuzGP09LvsQwOFVgPLjsSC7Ks66yLU5qMLqrzxFRUXYM0TqY18unD1EzMokXTkdtuRDddsW%2Bo%2BEjKq2Ay0iKrSpV8Azt7sM3JKBw1nYAz%2F6JhOvrDVOSyhirsrRtJ7Y0HpQlyfOmL3O4UivBfNMUxa1ciUnID9jJFjFGVBMDjI7Ah%2FRe9NIYLvsXOYznIKT1lZpt7zJ2jIN5QLq6KayT3dorIatmtP7YMyzXbovdtz7iEYeZ6pHaISchiJmWeiSsaXvJntiZWQfcSTbXmMPmzrzEjwU3ZJcVmn1f43BvyA9gIEhcDJHOjZp9X%2BNwb8gPYCBIXAyRzow%3D%3D","app_version":"8.3.4","os_version":"10.3.1","os_api":2,"mac":"0","width":375,"height":667,"imei":"0","idfa":"C98B99BB-1B2F-434E-BE53-FD651B03FB6A","openudid":"0","nt":4,"device_model":"iPhone8%2C1","device_brand":"0","language":"en-JP","display_density":"xhdpi","device_id":"766514487605914","video_play_time":0}
"""

if __name__ == "__main__":
    # res = requests.post(url_track, data=json.dumps(body_track),timeout=0.5)
    # print(res.json())
    headers = {'Content-type': "application/json"}
    # platform = raw_input("choose platform, 1-android;2-ios;0-stop: ").strip()
    platform = "1"
    data = body_ios
    if platform == "1":
        url = url.replace("https", "http")
        data = body_android
    for i in range(1):
        res = requests.post(url, data, headers=headers, timeout=0.5)
        print(json.dumps(res.json(), indent=4))