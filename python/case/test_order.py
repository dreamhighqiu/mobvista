# coding=UTF-8
import unittest
import requests
import json
from base.runmethod import RunMethod
from ddt import ddt,data,unpack
from util.logger import Logger
logger = Logger(logger="Order").getlog()

@ddt
class Order(unittest.TestCase):
    def setUp(self):
        self.runmain =RunMethod()
    @data("0","8","9")
    def test_GetUserOrders(self,status):
        url = "https://appapi-test.yaochufa.com/v2/Order/GetUserOrders"
        data = {
            "securityKey":
        "fPpxatGz1GRLdhlWUuCspp8IjXfYSW8qjhSWy4WFd%2Bd6nyIlF4SRFNCW7B6BqOqstWzhyz4TnFczVAFxSnmOvEAEjYqPLmFeefrpNyirU0XgY3DNutfJFDgXSn05Gcw1CwwSeh2AeT6v4SPgvOVUSCmgQ1V03Sim",
            "machineType":"0",
            "channel": "AppStore",
            "imei": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
            "lang": "app",
            "machineCode": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
            "system": "ios",
            "version":"5.9.1",
            "offset":"0",
            "orderStatus":status,
            "pageSize":"10"}
        res = self.runmain.run_main("GET", url=url, data=data)
        #print json.dumps(res,indent=2,ensure_ascii=True)
        print ("订单数---->>>>%s"%(res["data"]["total"]))
        items_key = res["data"]["items"]
        for i in range(len(items_key)):
            print ("订单ID----->>>%s"%(items_key[i]["orderId"]))
            print ("订单号----->>>%s"%(items_key[i]["orderNo"]))
            print ("订单状态----->>>%s"%(items_key[i]["orderStatus"]))

if __name__ == '__main__':
    unittest.main()
