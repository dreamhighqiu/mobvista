# encoding:utf-8

from file_utils import *
import json
RESULT = True
SET_DIFF_PARAM = set()


def cmp_dict_data_pass_diff(expect_dict, fact_dict, key_prefix="", set_pass=set(), set_diff=set(),
                            set_more=set(), set_less=set(), first_round=True):
    global SET_DIFF_PARAM, RESULT
    if first_round:
        SET_DIFF_PARAM = set()
        RESULT = True
    result = RESULT
    if expect_dict == fact_dict:
        return True, set()
    if not set_pass:
        set_pass = set()
    if not (expect_dict and fact_dict) or not(isinstance(expect_dict, dict) and isinstance(fact_dict, dict)):
        SET_DIFF_PARAM.add('illegal data')
        write_log('one side data is illegal, \n\texpect: {0}\t{1}\n\tfact:{2}\t{3}'.format(type(expect_dict), expect_dict, type(fact_dict), fact_dict))
        return False, set()
    set_expect_keys = set(expect_dict.keys())
    set_fact_keys = set(fact_dict.keys())
    set_cmp = set_expect_keys.union(set_fact_keys)
    for key in set_cmp:
        c_result = True
        cmp_key = str(key)
        if key_prefix:
            cmp_key = '{0}{1}'.format(key_prefix, key)
        if remove_str_digit(cmp_key) in set_pass:
            continue
        expect_v = expect_dict.get(key)
        fact_v = fact_dict.get(key)
        if expect_v != fact_v:
            if not isinstance(expect_v, dict):
                c_result = False
                SET_DIFF_PARAM.add(cmp_key)
                if not c_result:
                    try:
                        write_log('{0}:\n\texpect is : {1} {2}\n\tfact   is : {3} {4}'
                                  .format(cmp_key, type(expect_v), expect_v, type(fact_v), fact_v))
                    except Exception as e:
                        write_log('{0}:\n\texpect is : {1}\n\tfact   is : {2}'
                                  .format(cmp_key, type(expect_v), type(fact_v)))
                        write_log(e, 'error')
            if type(expect_v) == type(fact_v) and isinstance(expect_v, dict):
                c_result, x = cmp_dict_data_pass_diff(expect_v, fact_v, cmp_key+'.', set_pass, set_diff,
                            set_more, set_less, first_round=False)
            result = result and c_result
        RESULT = RESULT and result
    return RESULT, SET_DIFF_PARAM


def cmp_dict_type(dict_expect, dict_fact, list_pass=None):
    if not list_pass:
        list_pass = []
    result = True
    list_diff = []
    set_keys = set(dict_expect.keys()).intersection(set(dict_fact.keys()))
    for key in set_keys:
        expect_type = type(dict_expect.get(key))
        fact_type = type(dict_fact.get(key))
        if expect_type != fact_type and key not in list_pass:
            # if expect_type in (int,long,float) and fact_type in(unicode,str):
            result = False
            msg = 'key: %s\n\t expect_type: %s\n\t fact_type: %s\n' % (key, expect_type, fact_type)
            list_diff.append(msg)
            write_log(msg)
    return result, list_diff


def remove_str_digit(str_x):
    for x in str_x:
        if x.isdigit():
            str_x = str_x.replace(x, '')
    str_x = str_x.replace('..', '.*.')
    return str_x

def soup_dict(data_dict):
        """
        格式化dict
        :param data_dict:
        :return:
        """
        print(json.dumps(data_dict, indent=4, sort_keys=False, ensure_ascii=False))


def cmp_list(list_expect, list_fact, sort_key=None, ignore_order=True):
    if list_expect == list_fact:
        return True
    if not ignore_order:
        msg = 'is diff! \n' \
                    '\texpect is : {1} {2}\n' \
                    '\tfact   is : {3} {4}'.format(type(list_expect), list_expect, type(list_fact), list_fact)
        write_log(msg)
        return False
    list_expect = sorted(list(list_expect), key=sort_key)
    list_fact = sorted(list(list_fact), key=sort_key)
    if list_expect != list_expect:
        write_log('[WARN] diff, expect: {0},fact: {1}'.format(list_expect, list_fact))
        return False
    return True


def cmp_dict_list(expect_dict_list, fact_dict_list):
    result = cmp_list(expect_dict_list, fact_dict_list)
    if result:
        return True


def get_diff_set(set_expect, set_fact):
    result = True
    set_expect, set_fact = map(lambda x: set(x), (set_expect, set_fact))
    set_less = set_expect - set_fact
    set_more = set_fact - set_expect
    if set_less or set_more:
        result = False
    return result, set_more, set_less


def format_dict_data(origin_data, dict_parse):
    """
    将字典中内嵌的有字典组成的数组转化为字段放到根节点下,注意需要转化的字段一定是字典组成的数组
    :param origin_data: 原始字典
    :param dict_parse: 需要转化的数组字段名,多级以.间隔, 数组转化为字典依赖的主键字段,eg{'data.ads':'id'}
    :return: 转化后的字典new_dict
    """
    new_data = origin_data
    for k, v in dict_parse.items():
        list_k = k.split(".")
        parse_data = origin_data
        eval_expression = "new_data"
        key_name = "new_data"
        i = 0
        try:
            for c_k in list_k:
                i += 1
                if i < len(list_k):
                    eval_expression += "['{0}']".format(c_k)
                if i == len(list_k):
                    eval_expression += ".pop('{0}')".format(c_k)
                key_name += "['{0}']".format(c_k)
                parse_data = parse_data.get(c_k)
            eval(eval_expression)
            new_data[k] = {}
            for parse_dict in parse_data:
                if not isinstance(dict_parse, dict):
                    raise KeyError
                new_data[k][parse_dict.get(v)] = parse_dict
        except (KeyError, TypeError):
            write_log("{0} not exists, expression is : {1}".format(key_name, eval_expression), 'warn')
    return new_data

def lower_dict_key(odict):
    for k in odict.keys():
        if not k.islower():
            odict[k.lower()] = odict[k]
            odict.pop(k)
    return odict


if __name__ == "__main__":
    true = True
    false = False
    null = None
    # cmp respons
    import requests
    import json
    show_list = ["icon_url"]
    url = "/openapi/ad/v3?orientation=1&app_version_name=1.0&package_name=com.mobvista.sdk.demo&os_version=6.1&sign=489942276c3cf759447d81719c104b95&unit_id=492&app_id=24282&platform=1&tnum=1&ad_type=42&timezone=GMT%252B08%253A00&mnc=&ping_mode=1&install_ids=%5B177536538%5D&sdk_version=MAL_8.4.0&ttc_ids=%5B177536538%5D&req_type=1&zeusDebug=1&exclude_ids=%5B177536538%5D&brand=google&ad_num=1&click_mode=1&screen_size=540x960&mcc=&gp_version=8.1.73.S-all%2520%255B0%255D%2520%255BFP%255D%2520165518514&display_cids=%5B177536538%5D&offset=1&only_impression=1&ad_source_id=1&gaid=ee94a9ba-c079-4786-8867-2ab109ed5610&dvi=4BzuYk5uRUE0iAVAfURFiah9fnVFfAv0WozwDki0G0RMiUvMiavMiavMiav0WoztYrxBYFQ3%2BFQ3RUE0DFfrfAl2HU39Hn3BHalTD0zK&language=en&is_clever=1&useragent=Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36&model=Nexus%25205X&network_type=9"
    expect_url = "http://test-net.rayjump.com"+url
    fact_url = "http://adnet.rayjump.com"+url
    expect_res = requests.get(expect_url).json()
    expect_res = format_dict_data(expect_res, {"data.ads": "id"})
    fact_res = requests.get(fact_url).json()
    fact_res = format_dict_data(fact_res, {"data.ads": "id"})
    cmp_dict_data_pass_diff(expect_res, fact_res)

    # cmp_adserver_request
    # expect_ios = {"timestamp":1520241889,"appId":22050,"unitId":128,"scenario":"openapi_download","adTypeStr":"native","adNum":1,"imageSizeId":"SIZE_1200x627","requestType":"OPENAPI_V3","category":"UNKNOWN","platform":"IOS","osVersion":"9.3.5","sdkVersion":"mi_2.4.0","packageName":"com.tianye1.mvsdk","appVersionName":"2.4.0","appVersionCode":"","imei":"","mac":"","devId":"","deviceModel":"","screenSize":"0x0","orientation":"UNKNOWN","mnc":"202","mcc":"201","networkType":"NET_WIFI","language":"","ip":"39.109.124.93","adnServerIp":"192.168.1.185","countryCode":"HK","sessionId":"5a9d0ce14e52423c612d75e3","parentSessionId":"5a9d0ce14e52423c612d75e4","timezone":"","GP_version":"","adSourceList":["APIOFFER"],"googleAdvertisingId":"","osVersionCode":90305,"DEPRECATED_publisherType":"M","networkId":0,"requestId":"5a9d0ce14e52423c61d75e5a","unitSize":"","offset":1,"showedCampaignIdList":[177536538],"idfa":"35951D6A-DB66-47A1-8CD0-DB1E9E0D33CD","recallADNOffer":1,"trueNum":1,"preclickCampaignIds":[177536538],"deviceBrand":"apple","cityCode":390,"realAppId":0,"unSupportSdkTruenum":0,"ua":"Mozilla%2f5.0+(iPhone%253B+CPU+iPhone+OS+9_3_5+like+Mac+OS+X)+AppleWebKit%2f601.1.46+(KHTML%252C+like+Gecko)+Mobile%2f13G36","osVersionCodeV2":9030500,"ifSupportSeperateCreative":2,"videoVersion":"1.0","rankerInfo":"{\"power_rate\":0,\"charging\":\"1\",\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\"}"}
    # fact_ios = {"timestamp":1520241918,"appId":22050,"unitId":128,"scenario":"openapi","adTypeStr":"native","adNum":1,"imageSizeId":"UNKNOWN","requestType":"OPENAPI_V3","category":"UNKNOWN","platform":"IOS","osVersion":"9.3.5","sdkVersion":"MI_2.4.0","packageName":"com.tianye1.mvsdk","appVersionName":"2.4.0","appVersionCode":"","imei":"","mac":"","devId":"35951D6A-DB66-47A1-8CD0-DB1E9E0D33CD","deviceModel":"0","screenSize":"0x0","orientation":"UNKNOWN","mnc":"202","mcc":"201","networkType":"NET_WIFI","language":"","ip":"39.109.124.93","adnServerIp":"13.228.233.14","countryCode":"HK","sessionId":"5a9d0cfe4e52427730265e4d","parentSessionId":"5a9d0cfe4e52427730265e4e","GP_version":"","adSourceList":["APIOFFER"],"googleAdvertisingId":"","osVersionCode":0,"DEPRECATED_publisherType":"M","requestId":"5a9d0cfe4e52427730265e4c","recallADNOffer":1,"trueNum":1,"osVersionCodeV2":0,"ifSupportSeperateCreative":2,"videoVersion":"1.0","rankerInfo":"{\"power_rate\":0,\"charging\":1,\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\\u0000\"}"}
    expect_and = {"timestamp":1520327423,"appId":24282,"unitId":492,"scenario":"openapi","adTypeStr":"native","excludeIdSet":{"177536538":true},"adNum":1,"imageSizeId":"UNKNOWN","requestType":"OPENAPI_V3","category":"UNKNOWN","platform":"ANDROID","osVersion":"6.0.1","sdkVersion":"mal_8.4.0","packageName":"com.mobvista.sdk.demo","appVersionName":"1.0","appVersionCode":"1","imei":"35362607855670","mac":"020000000000","devId":"ccf785f98e92d84b","deviceModel":"nexus205x","screenSize":"540x960","orientation":"VERTICAL","mnc":"","mcc":"","networkType":"NET_WIFI","language":"en","ip":"39.109.124.93","adnServerIp":"192.168.1.185","countryCode":"HK","sessionId":"5a9e5aff4e52423c7832d75d","parentSessionId":"5a9e5aff4e52423c7832d75e","timezone":"GMT%2B08%3A00","GP_version":"8.1.73.S-all%20%5B0%5D%20%5BFP%5D%20165518514","adSourceList":["APIOFFER"],"googleAdvertisingId":"ee94a9ba-c079-4786-8867-2ab109ed5610","osVersionCode":23,"DEPRECATED_publisherType":"M","networkId":0,"requestId":"5a9e5aff4e52423c782d75fa","unitSize":"540x960","showedCampaignIdList":[177536538],"idfa":"","recallADNOffer":1,"trueNum":1,"preclickCampaignIds":[177536538],"installIdSet":{"177536538":true},"deviceBrand":"google","cityCode":390,"realAppId":0,"unSupportSdkTruenum":0,"ua":"Mozilla%2F5.0%20%28Linux%3B%20Android%206.0.1%3B%20Nexus%205X%20Build%2FMTC19T%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F60.0.3112.116%20Mobile%20Safari%2F537.36","osVersionCodeV2":6000100,"ifSupportSeperateCreative":2,"videoVersion":"","rankerInfo":"{\"power_rate\":0,\"charging\":0,\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\"}"}
    fact_and = {"timestamp":1520327455,"appId":24282,"unitId":492,"scenario":"openapi","adTypeStr":"native","adNum":1,"imageSizeId":"UNKNOWN","requestType":"OPENAPI_V3","category":"UNKNOWN","platform":"ANDROID","osVersion":"6.0.1","sdkVersion":"MAL_8.4.0","packageName":"com.mobvista.sdk.demo","appVersionName":"1.0","appVersionCode":"1","imei":"35362607855670","mac":"020000000000","devId":"","deviceModel":"Nexus%205X","screenSize":"540x960","orientation":"VERTICAL","mnc":"","mcc":"","networkType":"NET_WIFI","language":"en","ip":"39.109.124.93","adnServerIp":"13.228.233.14","countryCode":"HK","sessionId":"5a9e5b1f4e524215859fb305","parentSessionId":"5a9e5b1f4e524215859fb306","timezone":"GMT%2B08%3A00","GP_version":"","adSourceList":["APIOFFER"],"googleAdvertisingId":"ee94a9ba-c079-4786-8867-2ab109ed5610","osVersionCode":0,"DEPRECATED_publisherType":"M","networkId":0,"requestId":"5a9e5b1f4e524215859fb304","unitSize":"","idfa":"","recallADNOffer":1,"trueNum":1,"deviceBrand":"google","cityCode":390,"realAppId":0,"unSupportSdkTruenum":1,"ua":"Mozilla%2F5.0%20%28Linux%3B%20Android%206.0.1%3B%20Nexus%205X%20Build%2FMTC19T%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F60.0.3112.116%20Mobile%20Safari%2F537.36","osVersionCodeV2":0,"ifSupportSeperateCreative":2,"videoVersion":"","rankerInfo":"{\"power_rate\":0,\"charging\":0,\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\\u0000\"}"}
    # cmp_dict_data_pass_diff(expect_and, fact_and, "", {"timestamp","requestId","parentSessionId","sessionId"})

    # cmp ad_server_log
    # tailf /data/recommend/advanced_search/log/
    expect_adserver_log = {"1":{"i64":1520327342},"2":{"i64":24282},"3":{"i64":492},"4":{"str":"openapi"},"5":{"str":"native"},"6":{"set":["i64",1,177536538]},"7":{"i32":1},"8":{"i32":0},"9":{"i32":7},"10":{"i32":0},"11":{"i32":1},"12":{"str":"6.0.1"},"13":{"str":"mal_8.4.0"},"14":{"str":"com.mobvista.sdk.demo"},"15":{"str":"1.0"},"16":{"str":"1"},"17":{"str":"35362607855670"},"18":{"str":"020000000000"},"19":{"str":"ccf785f98e92d84b"},"20":{"str":"nexus205x"},"21":{"str":"540x960"},"22":{"i32":1},"23":{"str":""},"24":{"str":""},"25":{"i32":9},"26":{"str":"en"},"27":{"str":"39.109.124.93"},"28":{"str":"192.168.1.185"},"29":{"str":"HK"},"31":{"i32":0},"33":{"str":"5a9e5aae4e5242518d56f8f7"},"34":{"str":"5a9e5aae4e5242518d56f8f8"},"35":{"str":"GMT%2B08%3A00"},"36":{"str":"8.1.73.S-all%20%5B0%5D%20%5BFP%5D%20165518514"},"37":{"lst":["i32",1,1]},"39":{"str":"ee94a9ba-c079-4786-8867-2ab109ed5610"},"40":{"i32":23},"41":{"i32":3},"44":{"i64":0},"45":{"str":"5a9e5aae4e5242518d6f8f9a"},"46":{"str":"540x960"},"47":{"i32":0},"50":{"lst":["i64",1,177536538]},"52":{"str":""},"53":{"i32":1},"55":{"i64":1},"56":{"lst":["i64",1,177536538]},"57":{"set":["i64",1,177536538]},"59":{"str":"google"},"60":{"i64":390},"64":{"i64":0},"65":{"i32":0},"66":{"str":"Mozilla%2F5.0%20%28Linux%3B%20Android%206.0.1%3B%20Nexus%205X%20Build%2FMTC19T%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F60.0.3112.116%20Mobile%20Safari%2F537.36"},"68":{"i32":6000100},"69":{"i32":2},"70":{"str":""},"72":{"lst":["i64",0]},"75":{"str":"{\"power_rate\":0,\"charging\":0,\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\"}"},"666":{"i32":0}}
    fact_adserver_log = {"1":{"i64":1520327362},"2":{"i64":24282},"3":{"i64":492},"4":{"str":"openapi"},"5":{"str":"native"},"7":{"i32":1},"8":{"i32":0},"9":{"i32":7},"10":{"i32":0},"11":{"i32":1},"12":{"str":"6.0.1"},"13":{"str":"MAL_8.4.0"},"14":{"str":"com.mobvista.sdk.demo"},"15":{"str":"1.0"},"16":{"str":"1"},"17":{"str":"35362607855670"},"18":{"str":"020000000000"},"19":{"str":""},"20":{"str":"Nexus%205X"},"21":{"str":"540x960"},"22":{"i32":1},"23":{"str":""},"24":{"str":""},"25":{"i32":9},"26":{"str":"en"},"27":{"str":"39.109.124.93"},"28":{"str":"13.228.233.14"},"29":{"str":"HK"},"31":{"i32":0},"33":{"str":"5a9e5ac24e524215859fb300"},"34":{"str":"5a9e5ac24e524215859fb301"},"35":{"str":"GMT%2B08%3A00"},"36":{"str":""},"37":{"lst":["i32",1,1]},"39":{"str":"ee94a9ba-c079-4786-8867-2ab109ed5610"},"40":{"i32":0},"41":{"i32":3},"44":{"i64":0},"45":{"str":"5a9e5ac24e524215859fb2ff"},"46":{"str":""},"47":{"i32":0},"52":{"str":""},"53":{"i32":1},"55":{"i64":1},"59":{"str":"google"},"60":{"i64":390},"64":{"i64":0},"65":{"i32":1},"66":{"str":"Mozilla%2F5.0%20%28Linux%3B%20Android%206.0.1%3B%20Nexus%205X%20Build%2FMTC19T%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F60.0.3112.116%20Mobile%20Safari%2F537.36"},"68":{"i32":0},"69":{"i32":2},"70":{"str":""},"75":{"str":"{\"power_rate\":0,\"charging\":0,\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\\u0000\"}"},"666":{"i32":0}}
    # for i in range(1,76,1):
    #    print(expect_adserver_log.get(str(i)))
    # cmp_dict_data_pass_diff(expect_adserver_log, fact_adserver_log)

    # cmp final req_params
    corsair_req_params = {"appId":24282,"unitId":492,"sign":"489942276c3cf759447d81719c104b95","imageSizeId":0,"unitSize":"540x960","category":0,"adNum":1,"excludeIds":"[177536538]","excludeIdArr":[177536538],"installIdArr":[177536538],"offset":1,"pingMode":1,"scenario":"openapi","adType":"native","adTypeId":42,"requestType":7,"ip":"39.109.124.93","platformId":1,"osVersion":"6.0.1","packageName":"com.mobvista.sdk.demo","appVersionCode":"1","sdkVersion":"mal_8.4.0","googlePlayVersion":"8.1.73.S-all%20%5B0%5D%20%5BFP%5D%20165518514","orientation":1,"deviceModel":"nexus205x","mnc":"","mcc":"","networkTypeId":9,"language":"en","timezone":"GMT%2B08%3A00","useragent":"Mozilla%2F5.0%20%28Linux%3B%20Android%206.0.1%3B%20Nexus%205X%20Build%2FMTC19T%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F60.0.3112.116%20Mobile%20Safari%2F537.36","screenSize":"540x960","network":0,"impressionImage":"","onlyImpression":1,"adSourceId":1,"sessionId":"5a9f4f944e52423c6f1af510","parentSessionId":"5a9f4f944e52423c6f1af511","deviceBrand":"google","appVersionName":"1.0","googleAdvertisingId":"ee94a9ba-c079-4786-8867-2ab109ed5610","idfa":"","nativeInfoList":"","displayCids":"[177536538]","frameNum":1,"ttcIds":"[177536538]","trueNum":1,"unSupportSdkTruenum":0,"idfv":0,"openidfa":0,"priceFloor":"","httpReq":0,"realAppId":0,"isOffline":0,"requestTypeName":"","isClever":"1","videoVersion":"","videoW":0,"videoH":0,"ext_flowTagId":1,"flowRequestId":"5a9f4f944e52423c6faf512b","zeusDebug":"","versionFlag":0,"mwCityCode":0,"mwCountryCode":"","goAdserver":0,"apiVersion":0,"prePid":"","channel":0,"zeusRedisDebug":"","isVast":"","adFormat":1,"serverClever":"","networkStr":"","cache1":"","cache2":"","powerRate":0,"charging":0,"subIp":"","zeusRedisLocalDebug":"","ats":"","uiOrientation":0,"mainDomain":"","creativeRedisDebug":"","cc":"","systemUseragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/64.0.3282.186 Safari\/537.36","imei":"35362607855670","mac":"020000000000","devId":"ccf785f98e92d84b","lat":"","lng":"","gpst":"","gpsAccuracy":"","gpsType":"","cid":"","rankerInfo":"{\"power_rate\":0,\"charging\":0,\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\"}","countryCode":"HK","extra12":390,"cityString":"hong kong","imageSize":"128x128","networkType":"wifi","platform":"android","mobileCode":"","osVersionCode":23,"osVersionCodeV2":6000100,"baseIds":[],"serverId":"192.168.1.185","rand":"40","langNum":1,"remoteIp":"192.168.1.228","sdkType":"mal","sdkNumber":"8.4.0","MPSAClever":"","publisherId":5731,"publisherType":3,"devinfoEncrypt":1,"extra5":"5a9f4f944e52423c6faf512b","requestId":"5a9f4f944e52423c6faf512b","preClick":true,"extra13":1,"template":2,"extra16":2,"extra17":"0,0","isLinktypeTest":false,"extra15":1,"ext_cdnType":0,"newCreative":2,"endcard":{"url":"","id":0},"ext_endcard":0,"ext_finalPackageName":"id24282","ext_abtest1":0,"ext_channel":0,"ext_abtest2":0,"canGo3SCN":true,"extra4":"5a9f4f944e52423c6faf512b","MW_randValue":931,"MW_flowTagId":1,"adBackendConfig":"1:0:0","extra7":1,"adBackend":[1],"extra3":"MNormalAlphaModelRTestRanker_old_1.0.0;11;772;18;0;18;0;","algo":"","isMobvistaOnlyVba":null,"extra":"ad_server","ext_ifLowerImp":null,"backendId":1,"requestKey":"","rushNOPreclick":false,"ext_rushNoPre":0,"extra20":"[[130553083,457,0,0,1,1]]","extra2":"130553083","extra6":1,"ext_thirdCid":"","extra9":"Mozilla%252F5.0%2520%2528Linux%253B%2520Android%25206.0.1%253B%2520Nexus%25205X%2520Build%252FMTC19T%253B%2520wv%2529%2520AppleWebKit%252F537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Version%252F4.0%2520Chrome%252F60.0.3112.116%2520Mobile%2520Safari%252F537.36","ext_systemUseragent":"Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F64.0.3282.186%20Safari%2F537.36","ext_packageName":"com.mobvista.sdk.demo"}
    corsair_req_params = lower_dict_key(corsair_req_params)
    adnet_req_params = {"Param":{"RequestPath":"/openapi/ad/v3","RequestID":"5a9f49644e524277979a2e95","ClientIP":"39.109.124.93","RemoteIP":"","ServerIP":"","Platform":1,"OSVersion":"6.0.1","OSVersionCode":0,"PackageName":"com.mobvista.sdk.demo","AppVersionName":"1.0","AppVersionCode":"1","Orientation":1,"Brand":"google","Model":"Nexus%205X","AndroidID":"ccf785f98e92d84b","IMEI":"35362607855670","MAC":"020000000000","GAID":"ee94a9ba-c079-4786-8867-2ab109ed5610","IDFA":"","MNC":"","MCC":"","NetworkType":9,"Language":"en","TimeZone":"GMT%2B08%3A00","UserAgent":"Mozilla%2F5.0%20%28Linux%3B%20Android%206.0.1%3B%20Nexus%205X%20Build%2FMTC19T%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F60.0.3112.116%20Mobile%20Safari%2F537.36","SDKVersion":"MAL_8.4.0","GPVersion":"8.1.73.S-all%20%5B0%5D%20%5BFP%5D%20165518514","GPSV":"","ScreenSize":"540x960","LAT":"","LNG":"","GPST":"","GPSAccuracy":"","GPSType":0,"D1":"","D2":"","D3":"","AppID":24282,"UnitID":492,"PublisherID":5731,"PublisherType":3,"Sign":"489942276c3cf759447d81719c104b95","Category":0,"AdNum":1,"PingMode":1,"UnitSize":"","ExcludeIDS":"[177536538]","Offset":1,"SessionID":"","ParentSessionID":"","OnlyImpression":1,"NetWork":"","ImpressionImage":0,"AdSourceID":1,"AdType":42,"NativeInfo":"","RealAppID":0,"IsOffline":0,"Scenario":"openapi","TNum":1,"ImageSize":"","InstallIDS":"[177536538]","DisplayCIDS":"[177536538]","FrameNum":0,"TTCIDS":"[177536538]","IDFV":"","OpenIDFA":"","PriceFloor":0,"HTTPReq":0,"DVI":"4BzuYk5uRUE0iAVAfURFiah9fnVFfAv0WozwDki0G0RMiUvMiavMiavMiav0WoztYrxBYFQ3+FQ3RUE0DFfrfAl2HU39Hn3BHalTD0zK","Smart":"","Power":"","BaseIDS":"","FlowTagID":0,"CountryCode":"HK","CityCode":390,"RandValue":0,"ApiRequestNum":-2,"ApiCacheNum":-2,"VersionFlag":0,"VideoVersion":"","VideoAdType":1,"AppName":"Android7.4demo（donot modify）","ScreenWidth":540,"ScreenHeigh":960,"HeaderUA":"","UaFamily":"","RealPackageName":"id24282","Extra":"","Extra4":"","Extra7":0,"Extra8":0,"Extra13":0,"Extra14":0,"Extra16":0,"PowerRate":0,"Charging":0,"TotalMemory":"","ResidualMemory":"","CID":"","RankerInfo":"{\"power_rate\":0,\"charging\":0,\"total_memory\":\"\",\"residual_memory\":\"\",\"cid\":\"\",\"lat\":\"\",\"lng\":\"\",\"gpst\":\"\",\"gps_accuracy\":\"\",\"gps_type\":\"\\u0000\"}","ApiVersion":0,"DisplayCamIds":null,"UnSupportSdkTrueNum":1,"Network":0,"PreClickCamIds":null,"CreativeId":0,"IsRVBack":false,"EndcardCreativeID":0,"CreativeDescSource":0,"AlgoMap":null,"AdvertiserID":0,"CampaignID":0,"Extbtclass":0,"Extfinalsubid":0,"ExtdeleteDevid":"","ExtinstallFrom":"","Extstats":"","ExtpackageName":"","ExtnativeVideo":"","ExtflowTagId":"","ExtcdnType":"","Extendcard":"","ExtrushNoPre":"","ExtdspRealAppid":0,"ExtfinalPackageName":"","Extnativex":"","Extattr":"","Extstats2":"","Extadstacking":"","Extctype":0,"Extrvtemplate":0,"Extabtest1":"","ExtcreativeCdnFlag":"","ExtcreativeSizeFlag":"","Extplayable":"","ExtpriceIn":"","ExtpriceOut":"","Extb2t":"","Extchannel":"","ExtadvInstallTime":"","ExtthreesInstallTime":"","Extabtest2":"","Extbp":"","Extsource":"","Extreject":"","Extalgo":"","ExtthirdCid":"","ExtifLowerImp":"","Extnvt2":0,"ExttrueNvt2":"","MWRandValue":0,"MWFlowTagID":0,"Debug":0},"UnitInfo":{"unitId":492,"appId":24282,"app":{"appId":24282,"grade":1,"status":4,"created":1458111075,"platform":1,"isIncent":1,"directMarket":2,"name":"Android7.4demo（donot modify）","publisherId":5731,"campaignType":2,"custom":[],"devinfoEncrypt":1,"apkChance":{"ALL":0},"rushSetting":{"pc":50,"sdkrush":1}},"publisher":{"publisherId":5731,"username":"adntest","status":1,"forceDeviceId":2,"apiKey":"7c22942b749fe6a6e361b675e96b3ee9","blockCategory":[30],"type":3,"mvSourceStatus":1,"created":1438067413},"unit":{"isIncent":2,"btClass":0,"grade":0,"status":1,"adType":42,"videoAds":1,"unitId":492,"appId":24282,"publisherId":5731,"name":"youxian FB","orientation":1,"templates":[2,3],"preClick":true,"pubnativeAppToken":"","mobvistaAppId":24283,"mobvistaApiKey":"ce7599d6bb7eb5a0c098aabb6af64a2c","entraImage":"","relatedUnitId":0,"redPointShow":true,"redPointShowInterval":0,"apiRequestNum":-2,"apiCacheNum":-2,"ttcType":2,"newFakeRule":1,"adFilter":-2,"nvTemplate":0},"setting":{"apiRequestNum":-2,"apiCacheNum":-2,"ttcType":2},"blackPackageNameList":["ccc.ccc.ccc","com.asdfasfw","da.cdsadfsaf","com.cmcm.iswipe","ttt.cc.cc"],"outputType":[],"adSourceCountry":{"AD":0,"AE":0,"AF":0,"AG":0,"AI":0,"AL":0,"AM":0,"AO":0,"AQ":0,"AR":0,"AS":0,"AT":0,"AU":0,"AW":0,"AX":0,"AZ":0,"BA":0,"BB":0,"BD":0,"BE":0,"BF":0,"BG":0,"BH":0,"BI":0,"BJ":0,"BL":0,"BM":0,"BN":0,"BO":0,"BQ":0,"BR":0,"BS":0,"BT":0,"BV":0,"BW":0,"BY":0,"BZ":0,"CA":0,"CC":0,"CD":0,"CF":0,"CG":0,"CH":0,"CI":0,"CK":0,"CL":0,"CM":0,"CN":0,"CO":0,"CR":0,"CU":0,"CV":0,"CW":0,"CX":0,"CY":0,"CZ":0,"DE":0,"DJ":0,"DK":0,"DM":0,"DO":0,"DZ":0,"EC":0,"EE":0,"EG":0,"EH":0,"ER":0,"ES":0,"ET":0,"FI":0,"FJ":0,"FK":0,"FM":0,"FO":0,"FR":0,"GA":0,"GB":0,"GD":0,"GE":0,"GF":0,"GG":0,"GH":0,"GI":0,"GL":0,"GM":0,"GN":0,"GP":0,"GQ":0,"GR":0,"GS":0,"GT":0,"GU":0,"GW":0,"GY":0,"HK":0,"HM":0,"HN":0,"HR":0,"HT":0,"HU":0,"ID":0,"IE":0,"IL":0,"IM":0,"IN":0,"IO":0,"IQ":0,"IR":0,"IS":0,"IT":0,"JE":0,"JM":0,"JO":0,"JP":1,"KE":0,"KG":0,"KH":0,"KI":0,"KM":0,"KN":0,"KP":0,"KR":0,"KW":0,"KY":0,"KZ":0,"LA":0,"LB":0,"LC":0,"LI":0,"LK":0,"LR":0,"LS":0,"LT":0,"LU":0,"LV":0,"LY":0,"MA":0,"MC":0,"MD":0,"ME":0,"MF":0,"MG":0,"MH":0,"MK":0,"ML":0,"MM":0,"MN":0,"MO":0,"MP":0,"MQ":0,"MR":0,"MS":0,"MT":0,"MU":0,"MV":0,"MW":0,"MX":0,"MY":0,"MZ":0,"NA":0,"NC":0,"NE":0,"NF":0,"NG":0,"NI":0,"NK":0,"NL":0,"NO":0,"NP":0,"NR":0,"NU":0,"NZ":0,"OM":0,"OTH":0,"PA":0,"PE":0,"PF":0,"PG":0,"PH":0,"PK":0,"PL":0,"PM":0,"PN":0,"PR":0,"PS":0,"PT":0,"PW":0,"PY":0,"QA":0,"RE":0,"RO":0,"RS":0,"RU":0,"RW":0,"SA":0,"SB":0,"SC":0,"SD":0,"SE":0,"SG":0,"SH":0,"SI":0,"SJ":0,"SK":0,"SL":0,"SM":0,"SN":0,"SO":0,"SR":0,"SS":0,"ST":0,"SV":0,"SX":0,"SY":0,"SZ":0,"TC":0,"TD":0,"TF":0,"TG":0,"TH":0,"TJ":0,"TK":0,"TL":0,"TM":0,"TN":0,"TO":0,"TR":0,"TT":0,"TV":0,"TW":0,"TZ":0,"UA":0,"UG":0,"UK":0,"UM":0,"US":0,"UY":0,"UZ":0,"VA":0,"VC":0,"VE":0,"VG":0,"VI":0,"VN":0,"VU":0,"WF":0,"WS":0,"YE":0,"YT":0,"ZA":0,"ZM":0,"ZW":0},"adSourceData":[[{"adSourceId":3,"status":1,"priority":8},{"adSourceId":1,"status":1,"priority":7},{"adSourceId":2,"status":2,"priority":6},{"adSourceId":5,"status":0,"priority":5},{"adSourceId":6,"status":0,"priority":4},{"adSourceId":7,"status":0,"priority":3},{"adSourceId":8,"status":0,"priority":2},{"adSourceId":9,"status":2,"priority":1}],[{"adSourceId":1,"status":1,"priority":8},{"adSourceId":3,"status":1,"priority":7},{"adSourceId":2,"status":2,"priority":6},{"adSourceId":5,"status":0,"priority":5},{"adSourceId":6,"status":0,"priority":4},{"adSourceId":7,"status":0,"priority":3},{"adSourceId":8,"status":0,"priority":2},{"adSourceId":9,"status":2,"priority":1}]],"updated":1513848403,"publisherId":5731,"myOfferIdList":[],"virtualReward":{"name":"","exchange_rate":0,"static_reward":0},"callbackUrl":"","securityKey":"","subsidyRule":null,"fakeRule":{"install":0,"start":null,"status":0,"updated":""},"fakeRuleV2":null,"fillRateUnit":null,"vtaConfigUnit":null},"AppInfo":{"appId":24282,"publisherId":5731,"app":{"appId":24282,"grade":1,"status":4,"created":1458111075,"platform":1,"isIncent":1,"directMarket":2,"name":"Android7.4demo（donot modify）","publisherId":5731,"campaignType":2,"custom":[],"devinfoEncrypt":1,"apkChance":{"ALL":0},"rushSetting":{"pc":50,"sdkrush":1},"rushUnits":{"492":100}},"publisher":{"publisherId":5731,"username":"adntest","status":1,"forceDeviceId":2,"apiKey":"7c22942b749fe6a6e361b675e96b3ee9","blockCategory":[30],"type":3,"mvSourceStatus":1,"created":1438067413},"blackPackageNameList":["ccc.ccc.ccc","com.asdfasfw","da.cdsadfsaf","com.cmcm.iswipe","ttt.cc.cc"],"updated":1517992965,"blackList":null,"allowIp":null,"postbackM":0,"excludeSpecialType":[],"vbaConf":{"vbaClose":2,"vbaOption":[]},"landingPageVersion":[],"realPackageName":"id24282","reduceRule":{"priority":0,"install":0,"status":0,"start":0,"price":0},"vtaConfigApp":null,"fillRateApp":null,"blend_traffic":null,"priceAdjustmentApp":0,"reduceRuleV2":null},"PublisherInfo":{"publisherId":5731,"publisher":{"publisherId":5731,"username":"adntest","status":1,"forceDeviceId":2,"apiKey":"7c22942b749fe6a6e361b675e96b3ee9","blockCategory":[30],"type":3,"mvSourceStatus":1,"created":1438067413},"blackPackageNameList":["ccc.ccc.ccc","com.asdfasfw","da.cdsadfsaf","com.cmcm.iswipe","ttt.cc.cc"],"excludeAdvertiserIds":[],"updated":1513848403},"DebugInfo":""}
    adnet_req_params.update(adnet_req_params["Param"])
    adnet_req_params = lower_dict_key(adnet_req_params)
    # cmp_dict_data_pass_diff(corsair_req_params, adnet_req_params)
    key = "appversionname"
    # print(adnet_req_params.get(key))

    # cmp middle request_log
    corsar_req_log = {}
    adnet_req_log = {}
    # cmp_dict_data_pass_diff(corsar_req_log, adnet_req_log)

    # cmp final reqquest_log
    corsair_net_req_log = {}
    adnet_net_req_log = {}
    # cmp_dict_data_pass_diff(corsair_net_req_log, adnet_net_req_log)


	# cmp impression_log
	# todo

	# cmp click_log
	# todo

	# cmp pv_log
	# todo

	# cmp reporting_tracking_log
	# todo

	# cmp no_reporting_tracking_log
	# todo