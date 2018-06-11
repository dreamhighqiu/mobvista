# coding=UTF-8
import unittest
from base.runmethod import RunMethod
from util.logger import Logger
logger = Logger(logger="Product").getlog()

class Product(unittest.TestCase):
    def setUp(self):
        self.runmain =RunMethod()
    def test_GetCommonPackagesByLinkIdV424(self):
        url = "https://appapi-test.yaochufa.com/v2/ProductPackage/GetCommonPackagesByLinkIdV424"
        data = {"channel":"AppStore",
                "checkInDate":"2018-01-27",
                "checkOutDate":"2018-03-02",
                "imei":"F99067E6-F1EA-4451-8007-15BFDE5372B1",
                "isSelected":"false",
                "lang":"app",
                "linkId":"117616",
                "machineCode":"F99067E6-F1EA-4451-8007-15BFDE5372B1",
                 "machineType":"0",
                "system":"ios",
                "version":"5.9.1"}
        res = self.runmain.run_main("GET", url=url, data=data)
        #print json.dumps(res,indent=2,ensure_ascii=True)
        data=res["data"]
        logger.info(u"获取库存信息")
        for i in range(len(data)):
            print ("----------->>>>>u'获取分组名称'")
            print (data[i]["tagName"])
            packageInfos_key =data[i]["packageInfos"][0]
            print ("---------->>>>>>>>>>u'获取分组内的套餐名称'")

            for j in range(len(packageInfos_key)):
                print (packageInfos_key[j]["packageName"])

                print (packageInfos_key[j]["channelLinkId"])

                try:
                    count = packageInfos_key[j]["stockCount"]
                    print (count)
                    self.assertEqual(count,0)
                    print ("库存为0")
                except:
                    print ("库存不为0")
                packagePromotionInfos_key =packageInfos_key[j]["packagePromotionInfos"]
                print (type(packagePromotionInfos_key))
                '''print packagePromotionInfos_key["promotionInstruction"]
                print packagePromotionInfos_key["promotionLabel"]
                print packagePromotionInfos_key["promotionTitle"]'''

if __name__ == '__main__':
    unittest.main()
