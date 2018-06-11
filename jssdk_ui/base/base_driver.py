#coding=utf-8
import time
from appium import webdriver
from util.write_user_command import WriteUserCommand
class BaseDriver:
	def android_driver(self,i):

		#print "this is android_driver:",i
		#devices_name adb devices
		#port
		write_file = WriteUserCommand()
		devices = write_file.get_value('user_info_'+str(i),'deviceName')
		port = write_file.get_value('user_info_'+str(i),'port')
		capabilities = {
		  "platformName": "Android",
		  #"automationName":"UiAutomator2",
		  "deviceName": devices,
		 	# "deviceName": '85U8PBFE99999999',
		  "app": "E:\\Chrome_320208401.apk",

		  "noReset":"true",
		  "platforVersion":"5.1",
		  "appPackage":"cn.com.open.mooc"
		  #"newCommandTimeout":'180'
		}
		driver = webdriver.Remote("http://127.0.0.1:"+port+"/wd/hub",capabilities)
		# driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
		time.sleep(10)
		
		return driver

if __name__=='__main__':
	b=BaseDriver('i')
	b.android_driver()