# -*- coding: utf-8 -*-
'''
Created on ：2018/6/8:19:20

@author: yunxia.qiu
'''
from util import read_txt_to_list
from util import read_txt_to_dict
from util import read_to_columns_csv_to_list
from util import read_two_columns_csv_to_dict

print(read_txt_to_dict("jsondemo.json"))
print(read_to_columns_csv_to_list("demo.csv"))
print(read_two_columns_csv_to_dict("demo.csv"))

print(read_txt_to_list("test.txt"))