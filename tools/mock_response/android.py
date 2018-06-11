#coding=UTF-8
import json
import os
filename='android.txt'
orientation=0
playable_ads_without_video=1

endcard_url='http://interactive.mintegral.com/qa_task/t113/v2/0528joom-5316a8a9855b16bc4ddc88c9a91c8733.zip?' \
            'md5filename=5316a8a9855b16bc4ddc88c9a91c8733&foldername=0528joom'



def change_data(filename=filename,endcard_url=endcard_url,orientation=orientation,playable_ads_without_video=playable_ads_without_video):
    f1 = open(filename, 'r+')
    json_str = f1.read()
    dict_data = json.loads(json_str)
    # print(type(dict_data))
    # print(dict_data)
    dict_data['data']['ads'][0]["endcard_url"] =endcard_url
    dict_data['data']['ads'][0]['rv']['orientation']=orientation
    dict_data['data']['ads'][0]['playable_ads_without_video']=playable_ads_without_video
    # print(dict_data)
    end_data=json.dumps(dict_data)
    print(end_data)
    with open('newandroid.txt','w+') as wf:
        wf.write(end_data)

change_data()


