# coding=UTF-8
import unittest
import requests
import json
from base.runmethod import RunMethod
from ddt import ddt,data,unpack
from util.logger import Logger
logger = Logger(logger="Search").getlog()

@ddt
class Search(unittest.TestCase):
    def setUp(self):
        self.runmain =RunMethod()
    @data(("1","5.9.1","android"),("7","5.9.0","ios"),("6","5.8.5","android"),("4","5.8.1","ios"),("3","5.9.2","ios"))
    @unpack
    def test_search(self,sort,version,system):
        url = "https://search-test.yaochufa.com/ycf-search/solr/vproduct/search"
        data = {"city":"广州",
                "cityCode":"440100",
                "cityLat":"23.12004910207623",
                "cityLng":"	113.3076496751518",
                "isTagPage":"1",
                "lat":"	23.130153812009",
                "lng":"113.38068380563",
                "machineType":"0",
                "maxPrice":"999999",
                "minPrice":"0",
                "p":"1",
                "province":"",
                "s":"20",
                "sort":sort,
                "tagList":"6260",
                "tagNew":"",
                "channel": "AppStore",
                "imei": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
                "lang": "app",
                "machineCode": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
                "system": system,
                 "version": version
                }

        res = self.runmain.run_main("GET",url =url, data =data)
        #print json.dumps(res,indent=2,ensure_ascii=True)
        rows_key = res["data"]["rows"]
        #print type(rows_key)
        for i in range(len(rows_key)):
            print ("------>>>>>>获取省份以及省份下的城市")
            print  (rows_key[i]["province"])
            print  (rows_key[i]["city"])
            print  (rows_key[i]["channelLinkId"])
            print  (rows_key[i]["productId"])
            print  (rows_key[i]["productName"])



if __name__ == '__main__':
    unittest.main()
