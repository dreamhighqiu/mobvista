# -*- coding: utf-8 -*-
'''
Created on ：2018/7/6:12:54

@author: yunxia.qiu
'''
import re
src_json ='sourcehtmlxyz123\n\t456sourcehtml'
new_str = "88888888888888888888"
mid=re.search(r"sourcehtml([\S|\s|\w|\W|.]*)sourcehtml",src_json)
res =mid.group(1)
des= src_json.replace(res,new_str)
print(des)



