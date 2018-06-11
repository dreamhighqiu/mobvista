#coding=utf-8
import time
from appium import webdriver
#from util.write_user_command import WriteUserCommand
class BaseDriver_single:
	def android_driver(self):
		capabilities = {
		  "platformName": "Android",
		  "automationName":"UiAutomator2",
		  #"deviceName": devices,
		  "deviceName":"85U8PBFE99999999",
		  "app": "E:\\Chrome_320208401.apk",
		  "noReset":"true",
		  "platforVersion":"5.1",
		  #"appPackage":"cn.com.open.mooc"
		  #"newCommandTimeout":'180'
		}
		#driver = webdriver.Remote("http://127.0.0.1:"+port+"/wd/hub",capabilities)
		driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)

		time.sleep(10)
		
		return driver

if __name__=='__main__':
	b=BaseDriver_single()
	b.android_driver()