#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
招商信用卡微信公众号-小积分抽大奖活动，一次花9积分，每天50次
"""

import os
import sys
import time

import requests
import random
from requests.sessions import TooManyRedirects

from messageInfo import message, get_message_info

cookies = ''

# 最好抓包替换成自己的UA
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000730) NetType/4G Language/zh_CN'


requests.packages.urllib3.disable_warnings()

# ss = requests.session()

pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
t = time.time()

# 获取通知模块
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
if os.path.exists(cur_path + "/sendNotify.py"):
    from sendNotify import send
else:
    def send(title, content):
        pass
###################

ss = requests.session()
ss.max_redirects = 1
total_count: int = 0


def load_home():
    print("加载抽奖首页")
    url = 'https://weclub.xyk.cmbchina.com/SCRMActivity/new-point/home?activityCode=POI0000042&urlSign=0de2c50d36'
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cookie': cookies,
        'User-Agent': USER_AGENT,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    try:
        resp = ss.get(url=url, headers=header, timeout=30)
        if resp.status_code == 200:
            print("cookie有效，直接去抽奖")
            for i in range(1, 2):
                print(f"第【{1}】次抽奖")
                duration = random.randint(1, 5)
                print(f"等待【{duration}】秒")
                time.sleep(duration)
                draw_lottery()
    except TooManyRedirects as e:
        err_resp = e.response
        if err_resp.status_code == 302:
            location = err_resp.headers["Location"]
            set_cookie = err_resp.raw.headers.getlist('Set-Cookie')
            print(location)
            print(set_cookie)


def do_oauth():
    url = 'https://xyk.cmbchina.com/OauthPortal/v2/wechat/callback?oauth_id=837f45c0&callback_uri=https%3A%2F%2Fweclub.xyk.cmbchina.com%2FSCRMActivity%2Fnew-point%2Fhome%3FactivityCode%3DPOI0000042%26urlSign%3D0de2c50d36&response_type=code&scope=snsapi_userinfo&state=state'
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cookie': cookies,
        'User-Agent': USER_AGENT,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    resp = requests.get(url=url, headers=header)
    print(resp)


def draw_lottery():
    global total_count
    url = 'https://weclub.xyk.cmbchina.com/SCRMActivity/new-point/request/draw-lottery.json'
    data = {"activityCode": "POI0000042", "subId": 1445}
    resp = ss.post(url=url, data=data)
    if resp.status_code == 200:
        result = resp.json()
        code = result["respCode"]
        data = result["data"]
        if code == '1000':
            awardId = int(data["awardId"])
            awardName = data["awardName"]
            print(f"抽奖成功,获取【{awardName}】")
            if awardId == 15792:
                total_count = total_count + 6666
            elif awardId == 15793:
                total_count = total_count + 19
            elif awardId == 15794:
                total_count = total_count + 1
            elif awardId == 15795:
                total_count = total_count + 9
            elif awardId == 15796:
                total_count = total_count + 99
            elif awardId == 15797:
                total_count = total_count + 999


def start():
    # load_home()
    do_oauth()

if __name__ == '__main__':
    start()