# -*- coding: utf-8 -*-
'''
Created on ：2018/7/5:19:15

@author: yunxia.qiu
'''

import requests
import base64
import json
import re

def get_basic_data(url):
    download_url ="https://us01.rayjump.com/click?k=5b3acd162eada967aa40d67b&p" \
               "=NjAyOHwyODAwMHwwfDkwM3wyMTMxNDU3MjZ8MjQyNTE4NTU5OHxub3JtYWx8aW5uZXJhY3RpdmV8MzIweDQ4MHw4fGFuZHJvaWR8NC4yfHxndC1pOTA2MHx8fFBIfHwyfHxub3JtYWx8fGNvbS5iaXR0b3JyZW50LmNsaWVudHw2MzQ5Mjh8NWIzYWNkMTYyZWFkYTk2N2FhNDBkNjdifHx8fHx8NWIzYWNkMTYyZWFkYTk2N2FhNDBkNjdifDQ5LjE0NC4yMDYuMjE4fHx8fHx8MHwwfDVhYzE2NzUxLTdkZGUtNDlkNi1iMGNhLWUzMGVjMjRlODk0NHx8fHNhbXN1bmd8fHxyYW5rX21vZGVsX2NhbXB8fDF8fHwscnkscnd8eyJjYXJyaWVyIjoiMDMiLCJjaXR5Ijoic2FudGEgcm9zYSIsImN0eXBlIjoiMSIsInBhcnNlIjoiMCIsInJlcXR5cGUiOiJpIiwidHJhZmZpY190eXBlIjoiYXBwIiwidnRhIjoiMSJ9fDE1MzA1ODAyNDZ8fDlhNTFhNTMzNjI1YzEzYjk1ZTJmMzJlNjI4Zjk0NWQxfDIwNjgyN3x8fHx8fGNvbS5iaXR0b3JyZW50LmNsaWVudHx8fHx8fDIxMDM4NDc2NDUyNDc2MXx8fHx8fHx8fHwwfHx8fHx8fHx8WzAuOCwwLjgsMSwxXQ==&r=eyJnaWQiOiIiLCJ0cGlkIjoxMjAyLCJjcmF0IjoyLCJhZHZfY3JpZCI6ODQ4NDk1LCJpY2MiOjEsImdsaXN0IjoiMTA0LDI0MjUxODU1OTgsODQ4NDk1LDMyMHg0ODAifQ=="
    # url = "http://interactive.mintegral.com/qa_task/t182/v9/0620dspfullscreen03_2abebc/0620dspfullscreen03_2abebc.html"
    absolute_url = url.split("/")[-1]
    absolute_url = url.replace(absolute_url, "")
    res = requests.get(url)
    web_content = res.content
    web_content = web_content.replace("style/", absolute_url + "style/")
    web_content = web_content.replace("zepto.min.js", absolute_url + "zepto.min.js")
    web_content = web_content.replace("swiper.min.js", absolute_url + "swiper.min.js")
    web_content = web_content.replace("animate.js", absolute_url + "animate.js")
    web_content = web_content.replace("swiper.min.css", absolute_url + "swiper.min.css")
    web_content = web_content.replace("swiper.js", absolute_url + "swiper.js")
    web_content = web_content.replace("这是需要集成的下载链接", download_url)
    return web_content


def get_decode_template():
    pass

def get_template_date(url, src_json, des_json ):
    with open(src_json) as rf:
        json_content_str = rf.read()
        print(json_content_str)
    json_content_dict = json.loads(json_content_str)
    print(json_content_dict)
    template_content_list = json_content_dict.get("webview").get("elements")
    for i in template_content_list:
        if i.get("name") == "adm.js":
            src_template_content = i.get("value")
            template_content = base64.b64decode(src_template_content)
            #print(template_content)

            data_src = "<HTMLResource><![CDATA[]]>"
            basic_data = get_basic_data(url)
            data_dec = "<HTMLResource><![CDATA[%s]]>"%basic_data
            #print(data_dec)
            template_content = template_content.replace(data_src, data_dec)
            #print(template_content)
            encode_template_data = base64.b64encode(template_content)
            #print(encode_template_data)
            des_template_content = encode_template_data
            json_content_str = json_content_str.replace(src_template_content, des_template_content)

            print(json_content_str)
            with open(des_json, "w") as wf:
                wf.write(json_content_str)
            break


def run(list_urls, src_json, dest_path):
    for i in range(len(list_urls)):
        url = list_urls[i]

        get_template_date(url,src_json, dest_path%str(i+1))




if __name__ == "__main__":
    list_url = []
    des_json = "C:/Users/M/Desktop/dsp/newdsp/chartboost/chartboost_%s.json"
    url_1 = 'http://interactive.mintegral.com/qa_task/t176/v7/0620dspslider01_e02ec4/0620dspslider01_e02ec4.html'
    url_2 = 'http://interactive.mintegral.com/qa_task/t177/v9/0620dspslider02_6814a4/0620dspslider02_6814a4.html'
    url_3 = 'http://interactive.mintegral.com/qa_task/t178/v9/0620dspslider03_e009ac/0620dspslider03_e009ac.html'
    url_4 = 'http://interactive.mintegral.com/qa_task/t179/v9/0620dspslider04_efe90a/0620dspslider04_efe90a.html'
    url_5 = "http://interactive.mintegral.com/qa_task/t180/v11/0620dspfullscreen01_762a5f/0620dspfullscreen01_762a5f.html"
    url_6 = "http://interactive.mintegral.com/qa_task/t181/v13/0620dspfullscreen02_069ee7/0620dspfullscreen02_069ee7.html"
    url_7 = "http://interactive.mintegral.com/qa_task/t182/v12/0620dspfullscreen03_e68af5/0620dspfullscreen03_e68af5.html"
    url_8 = "http://interactive.mintegral.com/qa_task/t183/v12/0620dspfullscreen04_d7fcc0/0620dspfullscreen04_d7fcc0.html"
    url_9 = 'http://interactive.mintegral.com/qa_task/t184/v12/0620banner01_1faf97/0620banner01_1faf97.html'
    url_10 = 'http://interactive.mintegral.com/qa_task/t185/v19/0620banner02_7bfc5c/0620banner02_7bfc5c.html'
    url_11 = 'http://interactive.mintegral.com/qa_task/t186/v16/0620banner03_ccc1e2/0620banner03_ccc1e2.html'
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
    run(list_url, "chartboost_basic_data.json", des_json)

