# -*- coding: utf-8 -*-
'''
Created on ：2018/6/8:14:56

@author: yunxia.qiu
'''

from base_driver import BaseDriver
from util.get_by_local import GetByLocal
class jssdk_class():
    def __init__(self,i):
        dr = BaseDriver()
        self.driver =dr.android_driver(i)
        self.loc=GetByLocal(self.driver)


    def open_app(self,url):
        # 定位输入框
        self.input=self.loc.get_element('chrome_app','input_text')
        self.input.send_keys(url)

    def switch_js(self):
        list=self.driver.contexts
        for i in list:
            if i in 'webview':
                self.driver.switch_to.context(i)







