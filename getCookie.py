# coding:utf-8
import json
import requests
from requests.exceptions import SSLError
'''
本脚本用于获得glados账号认证的cookie。
获取cookie后，直接复制内容至签到脚本中即可。
需要自行填写邮箱地址至 mailaddress 。
'''
mailaddress = '预登陆的邮箱地址'

# 尝试登陆，成功后会在邮箱中收到登陆code
def TryToSignin():
    url = 'https://glados.rocks/api/authorization'
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua-platform": "\"Windows\"",
        "Referer": "https://glados.rocks/login",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    data = {
        "address": "{0}".format(mailaddress),
        "site": "glados.network"
    }
    try:
        response = session.post(url, headers=headers, json=data)
    except SSLError:  # 为避免开启系统代理后无法成功链接出现错误，这里尝试使用代理重新链接。
        response = session.post(url, headers=headers, json=data, proxies=proxies)
    # 在创建的session下用post发起登录请求，放入参数：请求登录的网址、请求头和登录参数。
    print(response.text)
    print(response.status_code)


def SigninWithCode():
    url = 'https://glados.rocks/api/login'
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua-platform": "\"Windows\"",
        "Referer": "https://glados.rocks/login",
        'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    data = {
        "method": "email", "site": "glados.network", "email": "{0}".format(mailaddress),
        "mailcode": "{0}".format(input("请输入邮箱中收到的code："))
    }
    try:
        response = session.post(url, headers=headers, json=data)
    except SSLError:
        response = session.post(url, headers=headers, json=data, proxies=proxies)

    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    cookies_str = json.dumps(cookies_dict)
    f = open('cookies.txt', 'w')  # cookie结果存储文件，可以更改。
    f.write(cookies_str)
    f.close()
    # 以上5行代码，是cookies存储。
    print(response.text)
    print(response.status_code)


if __name__ == '__main__':
    session = requests.session()
    proxies = {'http': '127.0.0.1:7890',  # clash默认的代理，为避免打开clash后脚本无法正确访问互联网，在出现问题后尝试用代理访问。如需要使用其他代理，可在这里同步更改。
               'https': '127.0.0.1:7890'}
    TryToSignin()
    SigninWithCode()
    # 运行成功后，在当前目录下的cookies.txt文件即为账号的cookie，可以直接使用cookie登陆而无需邮箱code。
    

