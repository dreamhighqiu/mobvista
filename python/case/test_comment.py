# coding=UTF-8
import unittest
import json
from base.runmethod import RunMethod
from util.logger import Logger
logger = Logger(logger="Comment").getlog()

class Comment(unittest.TestCase):
    def setUp(self):
        self.runmain =RunMethod()
    def test_GetProductCommentsWithTag(self):
        url = "https://appapi-test.yaochufa.com/v2/Comment/GetProductCommentsWithTag"
        data ={"pageIndex":"1",
               "productId":"20025",
               "tagId":"1" ,
               "tagType":"1" ,
               "channel": "AppStore",
               "imei": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
               "lang": "app",
               "machineCode": "F99067E6-F1EA-4451-8007-15BFDE5372B1",
               "machineType": "0",
               "system": "ios",
               "version": "5.9.1",
                "pageSize":"15"}
        res = self.runmain.run_main("GET", url=url, data=data)
        res1 = json.dumps(res, indent=2, ensure_ascii=True).decode("unicode_escape").encode("utf-8")
        #print res1
        logger.info(u"获取评论信息")
        personCount = res["data"]["personCount"]
        print (personCount)
        info_key = res["data"]["commentInfos"]
        for i in range(len(info_key)):
            print (info_key[i]["content"])
        #print type(info_key)
        fixedTags_key = res["data"]["fixedTags"]
        for j in range(len(fixedTags_key)):
            print (fixedTags_key[j]["desc"])
            print (fixedTags_key[j]["count"])

if __name__ == '__main__':
    unittest.main()

