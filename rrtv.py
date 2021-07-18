#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
人人视频APP-每日领会员
"""

import os
import sys
import time
import requests
from messageInfo import message, get_message_info

ss = requests.session()

tokens = []
# token,多个&分隔
RRTV_TOKENS = ''

if "RRTV_TOKENS" in os.environ and os.environ["RRTV_TOKENS"]:
    RRTV_TOKENS = os.environ['RRTV_TOKENS']
if RRTV_TOKENS:
    tokens = RRTV_TOKENS.split('&')

# 获取通知模块
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
if os.path.exists(cur_path + "/sendNotify.py"):
    from sendNotify import send
else:
    def send(title, content):
        pass
###################


def start():
    for tk in tokens:
        do_memeber_activity(tk)
        time.sleep(1)


def do_memeber_activity(tk):
    try:
        url = 'https://api.rr.tv/user/member/activity'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'clientVersion': '1.0.0',
            'token': tk,
            'Accept-Language': 'zh-cn',
            'Origin': 'https://mobile.rr.tv',
            'clientType': 'web',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 App/RRSPApp platform/iPhone AppVersion/5.6.1',
            'Referer': 'https://mobile.rr.tv/fe/',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        resp = ss.post(url=url, headers=header).json()
        print(resp)
        message(resp['msg'])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start()
    send('【人人视频APP】', get_message_info())
