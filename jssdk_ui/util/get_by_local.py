#coding=utf-8
from config.ParseConfigurationFile import ParseConfigfile
class GetByLocal:
	def __init__(self,driver):
		self.driver = driver
	def get_element(self,key,value):
		read_ini = ParseConfigfile()
		local = read_ini.getOptionValue(key,value)
		if local != None:
			by = local.split('>')[0]
			local_by = local.split('>')[1]

			try:
				if by == 'id':
					return self.driver.find_element_by_id(local_by)
				elif by == 'className':
					return self.driver.find_element_by_class_name(local_by)
				else:
					return self.driver.find_element_by_xpath(local_by)

			except:
				#self.driver.save_screenshot("../jpg/test02.png")
				return None
		else:
			return None


