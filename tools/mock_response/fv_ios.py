#coding=UTF-8
import json
import os
filename='fv_ios.txt'
is_ready=100
mute_mode=1
offset_max=10
video_interactive_type=-3
video_skip_time=-1
daily_play_cap=70
ad_type = 256
change_value={
    'is_ready':is_ready,
    'mute_mode':mute_mode,
    'video_interactive_type':video_interactive_type,
    'video_skip_time':video_skip_time,
    'daily_play_cap':daily_play_cap,
    'offset_max': offset_max,
    'ad_type':ad_type
}

def change_data(filename=filename,ad_type=ad_type,data=change_value):
    f1 = open(filename, 'r+')
    json_str = f1.read()
    dict_data = json.loads(json_str)
    # print(type(dict_data))
    # print(dict_data)
    if ad_type==94:
        dict_data['data']['setting']["is_ready"] = data['is_ready']
        dict_data['data']['setting']["mute_mode"] = data['mute_mode']
        dict_data['data']['setting']["video_interactive_type"] = data['video_interactive_type']
        dict_data['data']['setting']["video_skip_time"] = data['video_skip_time']
        dict_data['data']['setting']["daily_play_cap"] = data['daily_play_cap']
        dict_data['data']['setting']["offset_max"] = data['offset_max']
        dict_data['data']["ad_type"] = data['ad_type']
    else:
        dict_data['data']['setting']["is_ready"] = data['is_ready']
        dict_data['data']['setting']["mute_mode"] = data['mute_mode']
        dict_data['data']['setting']["daily_play_cap"] = data['daily_play_cap']
        dict_data['data']['setting']["offset_max"] = data['offset_max']
        dict_data['data']["ad_type"] = data['ad_type']


    print(dict_data)
    end_data=json.dumps(dict_data,ensure_ascii=True,sort_keys=True,indent=4)
    print(end_data)
    with open('fv_ios.txt','w+') as wf:
        wf.write(end_data)

change_data()


