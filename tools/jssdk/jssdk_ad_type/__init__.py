# -*- coding: utf-8 -*-
'''
Created on ：2018/6/5:12:57

@author: yunxia.qiu
'''

import sys
print(sys.path)
x = [r'E:/tools/jssdk/jssdk_ad_type', r'C:/WINDOWS/SYSTEM32/python27.zip', r'D:/install/python2/DLLs', 'D:/install/python2/lib', 'D:/install/python2/lib/plat-win', 'D:/install/python2/lib/lib-tk', 'D:/install/python2',
'D:/install/python2/lib/site-packages', 'D:/install/python2/lib/site-packages/appium_python_client-0.26-py2.7.egg', 'D:/install/python2/lib/site-packages/adntest-2.0-py2.7.egg']

for i in x:
    sys.path.append(i)
reload(sys)
print(sys.path)