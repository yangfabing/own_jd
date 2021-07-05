#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
领京豆-早起福利，每天8点前访问领取额外京豆奖励
"""

import os
import sys
import time

from jdCookie import getCk
from userAgent import userAgent
from messageInfo import get_message_info, message

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)

requests.packages.urllib3.disable_warnings()

ss = requests.session()

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


def start():
    print("### 领京豆-早起福利 ###")
    all_get_bean = 0
    starttime = time.perf_counter()  # 记录时间开始
    global cookiesList, userNameList, pinNameList
    cookiesList, userNameList, pinNameList = getCk.iscookie()
    for ck in cookiesList:
        message(f"账号：【{userNameList[cookiesList.index(ck)]}】")
        url = 'https://api.m.jd.com/client.action?functionId=morningGetBean&area=22_1930_50948_52157&body=%7B%22rnVersion%22%3A%224.7%22%2C%22fp%22%3A%22-1%22%2C%22eid%22%3A%22%22%2C%22shshshfp%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%7D&build=167724&client=apple&clientVersion=10.0.6&d_brand=apple&d_model=iPhone12%2C8&eid=eidI1aaf8122bas5nupxDQcTRriWjt7Slv2RSJ7qcn6zrB99mPt31yO9nye2dnwJ/OW%2BUUpYt6I0VSTk7xGpxEHp6sM62VYWXroGATSgQLrUZ4QHLjQw&isBackground=N&joycious=60&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=32280b23f8a48084816d8a6c577c6573c162c174&osVersion=14.4&partner=apple&rfs=0000&scope=01&screen=750%2A1334&sign=0c19e5962cea97520c1ef9a2e67dda60&st=1625354180413&sv=112&uemps=0-0&uts=0f31TVRjBSsqndu4/jgUPz6uymy50MQJSPYvHJMKdY9TUw/AQc1o/DLA/rOTDwEjG4Ar9s7IY4H6IPf3pAz7rkIVtEeW7XkXSOXGvEtHspPvqFlAueK%2B9dfB7ZbI91M9YYXBBk66bejZnH/W/xDy/aPsq2X3k4dUMOkS4j5GHKOGQO3o2U1rhx5O70ZrLaRm7Jy/DxCjm%2BdyfXX8v8rwKw%3D%3D&uuid=&wifiBssid='
        header = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-Hans-CN;q=1',
            'Host': 'api.m.jd.com'
        }
        try:
            resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
            message(resp['data']['bizMsg'])
            if int(resp['data']['awardResultFlag']) == 1:
                all_get_bean = all_get_bean + int(resp['data']['beanNum'])
                message(f"获得{resp['data']['beanNum']}京豆")
            time.sleep(0.5)
        except Exception as e:
            print(e)
            continue

    message(f"\n本次总累计获得：{all_get_bean} 京豆")
    endtime = time.perf_counter()  # 记录时间结束
    message("\n------- 总耗时 : %.03f 秒 seconds -------" % (endtime - starttime))
    send("【领京豆-早起福利】", get_message_info())


if __name__ == '__main__':
    start()
