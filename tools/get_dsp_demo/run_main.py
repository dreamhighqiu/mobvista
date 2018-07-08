# -*- coding: utf-8 -*-
'''
Created on ：2018/7/5:19:15

@author: yunxia.qiu
'''

from chartboost import run_chartboost
from mopub import run_mopub
from smaato import run_smaato

class runmain():
	def __init__(self,list_url,des_smaato_path,des_chartboost_path,des_mopub_path):
		self.url = list_url
		self.des_smaato_path = des_smaato_path
		self.des_chartboost_path=des_chartboost_path
		self.des_mopub_path=des_mopub_path
		
	def run_all(self):
		run_smaato(self.url,'smaato_src_data.json',self.des_smaato_path)
		run_mopub(self.url,self.des_mopub_path)
		run_chartboost(self.url,'chartboost_basic_data.json',self.des_chartboost_path)
		
		
if __name__ == "__main__":
	
	url_1='http://interactive.mintegral.com/qa_task/t176/v7/0620dspslider01_e02ec4/0620dspslider01_e02ec4.html'
	url_2='http://interactive.mintegral.com/qa_task/t177/v9/0620dspslider02_6814a4/0620dspslider02_6814a4.html'
	url_3='http://interactive.mintegral.com/qa_task/t178/v9/0620dspslider03_e009ac/0620dspslider03_e009ac.html'
	url_4='http://interactive.mintegral.com/qa_task/t179/v9/0620dspslider04_efe90a/0620dspslider04_efe90a.html'
	url_5="http://interactive.mintegral.com/qa_task/t180/v11/0620dspfullscreen01_762a5f/0620dspfullscreen01_762a5f.html"
	url_6="http://interactive.mintegral.com/qa_task/t181/v13/0620dspfullscreen02_069ee7/0620dspfullscreen02_069ee7.html"
	url_7="http://interactive.mintegral.com/qa_task/t182/v12/0620dspfullscreen03_e68af5/0620dspfullscreen03_e68af5.html"
	url_8="http://interactive.mintegral.com/qa_task/t183/v12/0620dspfullscreen04_d7fcc0/0620dspfullscreen04_d7fcc0.html"
	url_9='http://interactive.mintegral.com/qa_task/t184/v12/0620banner01_1faf97/0620banner01_1faf97.html'
	url_10='http://interactive.mintegral.com/qa_task/t185/v19/0620banner02_7bfc5c/0620banner02_7bfc5c.html'
	url_11='http://interactive.mintegral.com/qa_task/t186/v16/0620banner03_ccc1e2/0620banner03_ccc1e2.html'
	
	list_url=[]
	list_url.append(url_1)
	list_url.append(url_2)
	list_url.append(url_3)
	list_url.append(url_4)
	list_url.append(url_5)
	list_url.append(url_6)
	list_url.append(url_7)
	list_url.append(url_8)
	list_url.append(url_9)
	list_url.append(url_10)
	list_url.append(url_11)
	smatto_json = "H:/dsp/smaato/smaato_%s.json"
	mopub_html="H:/dsp/mopub/mopub_%s.html"
	chartboost_json="H:/dsp/chartboost/chartboost_%s.json"
	
	run = runmain(list_url,smatto_json,chartboost_json,mopub_html)
	run.run_all()
	
		
	
	

