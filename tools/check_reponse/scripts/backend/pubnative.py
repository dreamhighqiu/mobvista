import requests
import json

# url_android = "http://api.pubnative.net/api/v3/native?apptoken=4522dd711c7b4b1b927abc5dff3d0d70&os=android&osver=6.0.1&devicemodel=0&dnt=1&al=l&srvi=1&zoneid=1&coppa=0&mf=campaignid&ip=39.109.124.93&ua=Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36&adcount=1&bundleid=com.mobvista.sdk.demo&gid=ee94a9ba-c079-4786-8867-2ab109ed5610&gidmd5=8b2669d6c015edf0a896b873eb8c939c&gidsha1=efbfe04d7b8e66734e62d5aaf227d9628ba9a10f"
# url_android = "http://api.pubnative.net/api/v3/native?apptoken=4522dd711c7b4b1b927abc5dff3d0d70&os=android&osver=6.0.1&devicemodel=0&dnt=1&al=l&srvi=1&zoneid=1&coppa=0&mf=campaignid&ip=169.235.24.133&ua=Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36&adcount=1&bundleid=com.mobvista.sdk.demo&gid=ee94a9ba-c079-4786-8867-2ab109ed5610&gidmd5=8b2669d6c015edf0a896b873eb8c939c&gidsha1=efbfe04d7b8e66734e62d5aaf227d9628ba9a10f"
# url_ios = "https://api.pubnative.net/api/v3/native?apptoken=70bb613ae48045488ef7c8227969a599&adcount=2&os=ios&osver=9.3.5&devicemodel=iPhone6%252C2&dnt=1&al=l&srvi=1&zoneid=1&coppa=0&mf=campaignid&ip=169.235.24.133&ua=Mozilla%252f5.0%2B%28iPhone%25253B%2BCPU%2BiPhone%2BOS%2B9_3_5%2Blike%2BMac%2BOS%2BX%29%2BAppleWebKit%252f601.1.46%2B%28KHTML%25252C%2Blike%2BGecko%29%2BMobile%252f13G36&bundleid=414478124&idfa=35951D6A-DB66-47A1-8CD0-DB1E9E0D33CC&idfamd5=7c4e0d5730c3fb30871be702581ed68d&idfasha1=ae15a321aeda7ce5ecf654ae24bede9805c6b5c4&secure=https"
url_android = "http://api.pubnative.net/api/v3/native?apptoken=4522dd711c7b4b1b927abc5dff3d0d70&os=android&osver=6.0.1&devicemodel=0&dnt=1&al=l&srvi=1&zoneid=1&coppa=0&mf=campaignid&ip=122.226.185.80&ua=Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36&adcount=1&bundleid=com.mobvista.sdk.demo&gid=ee94a9ba-c079-4786-8867-2ab109ed5610&gidmd5=8b2669d6c015edf0a896b873eb8c939c&gidsha1=efbfe04d7b8e66734e62d5aaf227d9628ba9a10f"
url_ios = "https://api.pubnative.net/api/v3/native?apptoken=70bb613ae48045488ef7c8227969a599&os=ios&osver=9.3&devicemodel=iPhone7%2C2&dnt=1&al=l&srvi=1&zoneid=1&coppa=0&mf=campaignid&ip=211.49.151.133&ua=Mozilla%2F5.0+%28iPhone%3B+CPU+iPhone+OS+9_3+like+Mac+OS+X%29+AppleWebKit%2F601.1.46+%28KHTML%2C+like+Gecko%29+Mobile%2F13E233&adcount=1&bundleid=12345&idfa=CD21D49E-2BF2-4F7D-9842-3A0896CA8974&idfamd5=65f075ef00e8c0f09e7fb5bcc4c2e6c0&idfasha1=88196bdef1c965351a1bf2ea3d293a40d8f513ed&secure=https"
def get_res(url_type):
    if url_type == "1":
        url = url_android
    else:
        url = url_ios
    # print(url)
    res = requests.get(url)
    # assert res.status_code == 200
    assert res.json()
    # print(json.dumps(res.json(),indent=4))
    return res.json()

if __name__ == "__main__":
    while True:
        url_type = raw_input("choose sdk type, 1-android|2-ios: ")
        for i in range(1):
            print(i)
            res = get_res(url_type)
            print(res)
            if res.get('ads'):
                print(json.dumps(res,indent=4))
                break
