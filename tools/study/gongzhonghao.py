# -*- coding: utf-8 -*-
'''
Created on ：2018/6/8:19:20

@author: yunxia.qiu
'''
from appium import webdriver
import time

# 作者：上海-悠悠 QQ交流群：512200893

desired_caps = {
                'platformName': 'Android',
                'platformVersion': '5.1',
                'deviceName': '85U8PBFE99999999',
                'appPackage': 'com.tencent.mm',
                'appActivity': '.ui.LauncherUI',
               # 'automationName': 'Uiautomator2',
                'unicodeKeyboard': True,
                'resetKeyboard': True,
                'noReset': True,
                'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}
                }

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(10)

# 作者：上海-悠悠 QQ交流群：512200893

# 点微信首页搜索按钮
driver.find_element_by_accessibility_id("搜索").click()
# 输入内容搜索
time.sleep(3)
driver.find_element_by_id('com.tencent.mm:id/hx').send_keys("yoyoketang")
# 点开公众号
time.sleep(3)
driver.find_element_by_id('com.tencent.mm:id/l7').click()

# 点公众号菜单-精品分类
time.sleep(3)
driver.find_elements_by_id('com.tencent.mm:id/aaq')[0].click()


# 切换到webview
time.sleep(2)
print(driver.contexts)

driver.switch_to.context('WEBVIEW_com.tencent.mm:tools')
time.sleep(3)
handles=driver.window_handles
print(driver.current_window_handle)
#driver.switch_to.window(handles[1])
driver.switch_to_window(handles[1])
# 点webview上元素 目前有个问题会报找不到元素
driver.find_element_by_xpath(".//*[@id='namespace_1']/div[1]/div/div[2]").click()
time.sleep(2)
title=driver.find_elements_by_css_selector(".title js_title")
for c in title:
    print(c.text)
driver.quit()