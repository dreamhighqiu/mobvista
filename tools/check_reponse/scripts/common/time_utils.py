# encoding:utf-8
import time

def str_to_long(str_time):
    #中间过程，一般都需要将字符串转化为时间数组
    # print(time.strptime(str_time,'%Y-%m-%d %H:%M:%S'))
    #将"2011-09-28 10:00:00"转化为时间戳
    int_time = int(time.mktime(time.strptime(str_time,'%Y-%m-%d %H:%M:%S')))
    return int_time

def long_to_str(long_time):
    #将时间戳转化为localtime
    x = time.localtime(long_time)
    return time.strftime('%Y-%m-%d %H:%M:%S',x)

if __name__ == "__main__":
    while True:
        print('now is %s'%(int(time.time())))
        str_time = raw_input('input time param, like 2017-08-19 00:00:00 or 1502987400: ')
        if not str_time:
            break
        if str_time.isdigit():
            print(long_to_str(long(str_time)))
        else:
            print(str_to_long(str_time))

