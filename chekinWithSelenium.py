# coding:utf-8
import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
'''
自动签到脚本的selenium实现。
内部逻辑为模拟浏览器鼠标点击。
因需要运行浏览器模拟框架，运行效率不佳且容易因为网络延迟出现问题，故只做出模板供参考。
'''
def webOption():
    ch_options = webdriver.ChromeOptions()

    # 不加载图片,加快访问速度
    ch_options.add_experimental_option("prefs", {"profile.mamaged_default_content_settings.images": 2})
    ch_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    ch_options.add_argument('--headless')  # 无头模式，可不启用界面显示运行，调试时可以打开
    # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # ch_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
    ch_options.add_argument('--proxy--server=127.0.0.1:8080')  # 代理设置，如不使用代理，去掉即可。
    ch_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    ch_options.add_argument('--incognito')  # 隐身模式（无痕模式）
    # browser = webdriver.Chrome(options=ch_options)
    return ch_options
def morning_clockin(options):
    # 找到插件的路径，使用它驱动操作
    s = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
    browser = webdriver.Chrome(service=s, options=options)

    # 选择需要打卡的网址，填入你的签到网页
    browser.get('https://glados.rocks')
    # 首先清除由于浏览器打开已有的cookies
    browser.delete_all_cookies()
    browser.refresh()
    with open('cookies.txt', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        # for cookie in cookies_list:
        #     browser.add_cookie(cookie)
        # cookie中的expiry字段可能会导致问题，所以不管会不会有问题处理掉完事。
        # 方法1 将expiry类型变为int
        # for cookie in cookies_list:
        #     # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
        #     if isinstance(cookie.get('expiry'), float):
        #         cookie['expiry'] = int(cookie['expiry'])
        #     driver.add_cookie(cookie)
        # 方法2删除该字段
        for cookie in cookies_list:
            # 该字段有问题所以删除就可以
            if 'expiry' in cookie:
                del cookie['expiry']
            browser.add_cookie(cookie)
    browser.refresh()
    time.sleep(5)
    browser.find_element(By.XPATH, '//a[@href="/login"]').click()
    time.sleep(4)
    # browser.find_element(By.XPATH, '//div[contains(text(),"签到")]').click()
    # browser.find_element(By.LINK_TEXT, '会员签到').click()
    browser.find_element(By.XPATH, '//*[@id="m4"]/i[@class="green calendar icon"]').click()
    # '/html/body/div/div/div/div/div[2]/div[2]/div/div/div[3]/div[5] //*[@id="m4"]/div/div[contains(text()="签到")]'
    time.sleep(3)
    browser.find_element(By.XPATH, '//button[contains(text(),"签到")]').click()
    # 找到邮件和密码输入框的xpath,并在对应的位置送入账号密码
    # browser.find_element_by_xpath('//*[@id="email"]').send_keys("724183***@qq.com")
    # browser.find_element_by_xpath('//*[@id="passwd"]').send_keys("zhan******")

    # 找到登录按钮的xpath，模拟点击
    # browser.find_element_by_xpath('//*[@id="login"]').click()
    time.sleep(2)
    # 找到签到按钮的xpath，模拟签到
    # browser.find_element_by_xpath('/html/body/div[3]/div[7]/div/button').click()


if __name__ == '__main__':
    today = datetime.datetime.now().weekday() + 1
    print(datetime.datetime.now())
    random_time = random.randint(0, 3)
    time.sleep(random_time)
    # 进行打卡
    morning_clockin(webOption())
    print(datetime.datetime.now())






