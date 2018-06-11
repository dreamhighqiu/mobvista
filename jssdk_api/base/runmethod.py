#coding:utf-8
import requests
import json
class RunMethod(object):
	def post_main(self,url,data,header=None):
		res = None
		if header !=None:	
			res = requests.post(url=url,verify=False,data=data,headers=header)
		else:
			res = requests.post(url=url,verify=False,data=data)
		return res.json()

	def get_main(self,url,data=None,header=None):
		res = None
		if header !=None:	
			res = requests.get(url=url,verify=False,params=data,headers=header)
		else:
			res = requests.get(url=url,verify=False,params=data)
		return res.json()

	def run_main(self,method,url,data=None,header=None):
		res = None
		if method == 'Post':
			res = self.post_main(url,data=data,header=header)
		else:
			res = self.get_main(url,data=data,header=header)
		return res
		#return json.dumps(res,ensure_ascii=False)
		#return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)
