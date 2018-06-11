# coding:utf-8


# 是否打印日志到控制台
PRINT_TO_CONSOLE = True
# 比对字典跳过的key，打印不同的信息，但是结果不依赖于这些key
LIST_IGNORE_KEY = ["notice_url", "data.only_impression_url"]
# 比对过程中不同的字典
DICT_DIFF_PARAM = {}
# 请求url所在文件的类型
# 1-txt已逗号间隔client_ip和参数url
# 2-csv
# 3-nginx日志
URL_FILE_TYPE = 1
# 接口模板

BACKEND_CONFIG = {
    "v3": {
        1: {
            "name": "mobvista",
            "host": "adnet.rayjump.com",
            "url": "http://{0}/openapi/ad/v3?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/response_{0}.json",
            "set_pass": {"data.session_id", "data.parent_session_id"}
        },
        0: {
            "name": "net",
            "host": "test-net.rayjump.com",
            "url": "http://{0}/openapi/ad/v3?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/response_{0}.json",
            "set_pass": {"data.session_id", "data.parent_session_id"}
        },
        2: {
            "name": "imobile",
            "host": "spnativeapi.i-mobile.co.jp",
            "url": "http://{0}/api/ad_native.ashx?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": set()
        },
        3: {
            "name": "adinall",
            "host": "app-test.adinall.com",
            "url": "http://{0}//api.m?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": set()
        },
        4: {
            "name": "inmobi",
            "host": "api.w.inmobi.com",
            "url": "http://{0}//showad/v3.1?",
            "method": "get",
            "headers": {"Content-Type": "application/json"},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": set()
        },
        5: {
            "name": "smatto",
            "host": "soma.smaato.net",
            "url": "http://{0}/openapi/ad/v3?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": set()
        },
        6: {
            "name": "pubnative",
            "host": "api.pubnative.net",
            "url": "http://{0}/openapi/ad/v3?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": set()
        },
        7: {
            "name": "leiting",
            "host": "logmonitor.leiting.com",
            "url": "http://{0}/openapi/ad/v3?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": set()
        },
        8: {
            "name": "toutiao",
            "host": "test-midway.rayjump.com",
            "url": "http://{0}/openapi/ad/v3?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": set()
        }
    },
    "ads": {
        0: {
            "name": "corsair",
            "host": "pre-net.rayjump.com",
            "url": "http://{0}/openapi/ads?",
            "method": "get",
            "request_data_type": "csv",
            "request_data_path": "data/ads/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/ads/response_{0}.json",
            "set_pass": set()
        },
        1: {
            "name": "net",
            "host": "pre-net24.rayjump.com",
            "url": "http://{0}/openapi/ads?",
            "method": "get",
            "request_data_type": "csv",
            "request_data_path": "data/ads/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/ads/response_{0}.json",
            "set_pass": set()
        }
    },
    "v2": {
        1: {
            "name": "mobvista",
            "host": "pre-midway.rayjump.com",
            "url": "http://{0}/openapi/ad/v2?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": {"data.session_id", "data.parent_session_id"}
        },
        0: {
            "name": "net",
            "host": "pre-net.rayjump.com",
            "url": "http://{0}/openapi/ad/v2?",
            "method": "get",
            "headers": {},
            "request_data_type": "csv",
            "request_data_path": "data/v3/mobvista/request_{0}.csv",
            "response_data_type": "json",
            "response_data_path": "data/v3/mobvista/response_{0}.json",
            "set_pass": {"data.session_id", "data.parent_session_id"}
        }
    }

}
backend_url = {
    "1": "http://{0}/openapi/ad/v3?{1}",
    "2": "http://api.w.inmobi.com/showad/v3.1"
}

backend_host = {
    "1": "test-net.rayjump.com"
}
