# coding=UTF-8
import unittest,json
from base.runmethod import RunMethod
from util.logger import Logger
logger = Logger(logger="HomePage").getlog()
class HomePage(unittest.TestCase):
    def setUp(self):
        self.runmain =RunMethod()
    def test_mergeConfig(self):
        url ="https://apiphp-test.yaochufa.com/api/common/mergeConfig"
        data = {"channel":"AppStore",
                "imei":"F99067E6-F1EA-4451-8007-15BFDE5372B1",
                "lang":"app",
                "machineCode":"F99067E6-F1EA-4451-8007-15BFDE5372B1",
                "machineType":"0",
                "system":"ios",
                "version":"5.9.1"}
        res = self.runmain.run_main("GET",url=url,data =data)
        res1 = json.dumps(res,indent=2,ensure_ascii=True).decode("unicode_escape").encode("utf-8")
        #print res1
        lyk_key=res["content"]["yfkConfig"]
        logger.info(u"获取旅游卡的开关状态")
        lyk_status = lyk_key["isShowYfk"]

        #print  element["yfkTipsMsg"]
        try:
            self.assertEqual(lyk_status,1)
            logger.info(u"获取旅游卡开启信息")
            print ("旅游卡开启")
        except:
            print ("旅游卡关闭")
        pay_key = res["content"]["paySucShareConfig"]
        pay_status = pay_key["isOpen"]

        try:
            self.assertTrue(pay_status)
            logger.info(u"获取支付后分享功能")
            print ("开启支付后分享活动功能")
        except:
            print ("关闭支付后分享活动功能")

    def test_qualitySimple(self):
        url ="https://apiphp-test.yaochufa.com/playpoint/qualitySimple"
        data = {"channel": "AppStore",
                "cityCode": "440100",
                "currentCityCode": "440100",
                "deviceToken": "5a52db122cabbe24b13bfdc473c54ae861c52ec1a0bb42fb78b2d93c1d4f8cda",
                "imei": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
                "lang": "app",
                "latitude": "23.130113745866",
                "longitude": "113.38075058426",
                "machineCode": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
                "machineType": "0",
                "pageIndex": "1",
                "system": "ios",
                "version": "5.9.1"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        res = self.runmain.run_main("GET", url=url, data=data, header=headers)
        #print json.dumps(res,indent=2,ensure_ascii=True).decode("unicode_escape").encode("utf-8")
        total = res["content"]["total"]
        print (total)
        try:
            self.assertEqual(total,"80")
            print ("周边游酒景个数未超过80个")
        except:
            print ("周边游酒景个数等于80个")
        city_key=res["content"]["content"]

        logger.info(u"获取酒景链接")
        logger.info(u"获取酒景ID")
        logger.info(u"获取酒景名称")
        logger.info(u"获取酒景城市")
        for i in range(len(city_key)):
            print ("------>>>>>>>>")
            print (city_key[i]["channelLinkId"])
            print (city_key[i]["productId"])
            print (city_key[i]["productName"])
            print (city_key[i]["cityName"])

            try:
                productName = city_key[i]["productName"]
                self.assertIn(u"测试",productName)
                print ("获取酒景中含有测试")
            except:
                print ("获取酒景中不包含测试")


if __name__ == '__main__':
    unittest.main()
