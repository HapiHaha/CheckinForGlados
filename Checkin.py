# coding:utf-8
import sys
import requests
from requests.exceptions import SSLError
import random
import time
import json
import datetime

'''
需要自行更改的变量：
cookie：登陆glados网页后账号对应的cookie，经两周的测试，同账号对应的cookie不会改变。
serverkey：通过server酱脚本可以将运行结果发到微信上，便于查看。如不需要使用，可将serverEn设为0.
serverEn：是否启用server酱上报结果，1启用，0关闭。
'''
cookie = '请输入你账号的cookie'
serverkey = '请输入server酱的key'
serverEn = 1
def dailyCheckin():
    url = 'https://glados.rocks/api/user/checkin' # glados网站签到使用的url
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua-platform": "\"Windows\"",
        "cookie": "{0}".format(cookie),   # cookie需要自行填写
        'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    data = {
        "token": "glados.network"
    }
    global result
    try:
        response = session.post(url, headers=headers, json=data)
    except SSLError: # 为避免开启系统代理后无法成功链接出现错误，这里尝试使用代理重新链接。
        session.proxies = proxies
        response = session.post(url, headers=headers, json=data, proxies=proxies)
    # print(response.text)
    dict = json.loads(response.text) # 获取返回的信息，其中message还有结果信息
    if 'Checkin' in dict['message']:
        result = 1
    elif 'Tomorrow' in dict['message']:
        result = -1

    print(dict['message'])
    print(response.status_code)
    return response.status_code

def WechatSend(title, desp, key):
    url = 'https://sctapi.ftqq.com/{0}.send'.format(key) # server酱使用的url，key需自行填写
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "title": "{0}".format(title), # 传给微信的标题
        "desp": "{0}".format(desp) # 传给微信的内容
    }
    try:
        response = requests.post(url, headers=headers, params=data)
    except SSLError:
        response = requests.post(url, headers=headers, params=data, proxies=proxies)
    # print(response.text)
    dict = json.loads(response.text)
    print(dict['data'])
    print(response.status_code)

if __name__ == '__main__':
    time1 = datetime.datetime.now()
    print('====='+str(time1)+'=====')
    random_time = random.random() * 360
    print(random_time)
    time.sleep(random_time) # 做一个简单时间随机，虽然glados应该没有机器人签到的限制，大概没什么意义。。
    result = 0
    session = requests.session()
    proxies = {'http': '127.0.0.1:7890',  # clash默认的代理，为避免打开clash后脚本无法正确访问互联网，在出现问题后尝试用代理访问。如需要使用其他代理，可在这里同步更改。
               'https': '127.0.0.1:7890'}
    retcode = dailyCheckin() # 签到
    if(serverEn == 0): # 如不需要server酱上报，输出结果。
        print('返回代码为'+retcode+'运行结果为：'+result)
        sys.exit(0)

    if(retcode != 200):
        title = '签到错误'
        desp = '发送签到POST时未得到200相应'
    elif result == 1 :
        title = '签到成功'
        desp = 'Checkin!'
    elif result == 0:
        title = '签到失败'
        desp = '得到回复但未回复Checkin!或Try Tomorrow，请自行确认是否成功签到'
    elif result == -1:
        title = '重复签到'
        desp = '今天已签到过，try tomorrow'
    WechatSend(title, desp, serverkey)
    sys.exit(0)
   


