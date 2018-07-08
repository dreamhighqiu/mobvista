# -*- coding: utf-8 -*-
'''
Created on ：2018/7/6:12:54

@author: yunxia.qiu
'''
# import re
# src_json ='sourcehtmlxyz123\n\t456sourcehtml'
# new_str = "88888888888888888888"
# mid=re.search(r"sourcehtml([\S|\s|\w|\W|.]*)sourcehtml",src_json)
# res =mid.group(1)
# des= src_json.replace(res,new_str)
# print(des)
#
import re
def read_html(src_path):
	with open(src_path,"r") as rf:
		result=rf.read()
		reg=r"<HTMLResource>[\s|\S]*</HTMLResource>"
	
	data_src=re.findall(reg, result)
	print(data_src)
read_html("test.html")



