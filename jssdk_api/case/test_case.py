# -*- coding: utf-8 -*-
'''
Created on ：2018/6/8:10:40

@author: yunxia.qiu
'''
from jssdk_bv import jssdk_banner_video
from jssdk_fv import fv_video
from jssdk_nv import jssdk_native_video
from net_v3 import net_v3
from ads_v3 import ads_v3
import unittest
import HTMLTestRunner_jpg
import os
class test_class(unittest.TestCase):


    def setUp(self):
        self.bv=jssdk_banner_video(10)
        self.fv=fv_video(10)
        self.nv=jssdk_native_video(10)
        self.ads_v3=ads_v3(10)
        self.net_v3=net_v3(10)

    def test_fv(self):
        self.fv.change_params()
        self.fv.req_data()

    def test_bv(self):
        self.bv.change_params()
        self.bv.req_data()
    def test_nv(self):
        self.nv.change_params()
        self.nv.req_data()
    def test_ads_v3(self):
        self.ads_v3.change_params()
        self.ads_v3.req_data()
    def test_net_v3(self):
        self.net_v3.change_params()
        self.net_v3.req_data()



