# coding=UTF-8
import unittest
import requests
import json
from base.runmethod import RunMethod
from ddt import ddt,data,unpack
from util.logger import Logger
logger = Logger(logger="Userinfo").getlog()


class Userinfo(unittest.TestCase):
    def setUp(self):
        self.runmain =RunMethod()
    def test_UserProfile(self):
        url = "https://appapi-test.yaochufa.com/v2/User/UserProfile"
        data = {
            "securityKey":
        "fPpxatGz1GRLdhlWUuCspp8IjXfYSW8qjhSWy4WFd%2Bd6nyIlF4SRFNCW7B6BqOqstWzhyz4TnFczVAFxSnmOvEAEjYqPLmFeefrpNyirU0XgY3DNutfJFDgXSn05Gcw1CwwSeh2AeT6v4SPgvOVUSCmgQ1V03Sim",
            "userId":"3228804" ,
            "machineType":"0",
            "channel": "AppStore",
            "imei": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
            "lang": "app",
            "machineCode": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
            "system": "ios",
            "version":"5.9.1"
        }
        res = self.runmain.run_main("GET", url=url, data=data)
        #print json.dumps(res,indent=2,ensure_ascii=True)
        #self.assertEqual(True, False)
        print (res["data"]["prePayCardTotalAmount"])
        print ("旅游卡金额%s"%(res["data"]["prePayCardTotalAmount"]))
        print ("微信ID%s"%(res["data"]["wxUserInfo"].decode("unicode_escape").encode("utf-8")))
        print ("积分数%s"%(res["data"]["credits"]))
        print ("总的订单数%s"%(res["data"]["orderCount"]))
        member = res["data"]["memberLevelName"]
        '''print "未支付订单数%s"%(res["data"]["orderCount"].decode("unicode_escape").encode("utf-8"))
        print "已支付订单数%s"%(res["data"]["orderPaidCoun"].decode("unicode_escape").encode("utf-8"))
        print "待出行订单数%s"%(res["data"]["orderReviewedCount"].decode("unicode_escape").encode("utf-8"))
        print "取消订单数%s"%(res["data"]["paidUnCancelOrderCoun"].decode("unicode_escape").encode("utf-8"))'''
        self.assertEqual(u"钻石会员",member)
        lyk = res["data"]["prePayCardTotalAmount"]
        if lyk>1000:
            print ("旅游卡超过1000元")
        else:
            print ("旅游卡金额少于1000元")





if __name__ == '__main__':
    unittest.main()
