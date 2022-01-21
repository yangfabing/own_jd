#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
bjxdAPP，粉丝日积分雨

20 13,16,19 20 * *

"""

import os
import sys
import time
import requests
import random
from messageInfo import message, get_message_info
import execjs
import multiprocessing

tokens = []
BM2_TOKENS = ''
if "BM2_TOKENS" in os.environ and os.environ["BM2_TOKENS"]:
    BM2_TOKENS = os.environ['BM2_TOKENS']
if BM2_TOKENS:
    tokens = BM2_TOKENS.split('&')

# 获取通知模块
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
if os.path.exists(cur_path + "/sendNotify.py"):
    from sendNotify import send
else:
    def send(title, content):
        pass


###################

def start(tk):
    ss = requests.session()
    do_play(tk, ss)


def do_play(tk, ss):
    try:
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/duiba/auto_login'
        header = {
            'App-Version': '8.5.0',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'token': tk,
            'User-Agent': 'ModernCar/8.5.0 (iPhone; iOS 14.1; Scale/2.00)',
            'Connection': 'keep-alive',
            'Referer': 'https://bm2-wx.bluemembers.com.cn/app/lottery',
            'device': 'iOS',
            'Origin-Id': 'D25BD59F-75AC-4D70-AE10-3DB6C4173858'
        }

        body = {
            'redirect': 'https://72596.activity-17.m.duiba.com.cn/projectx/p30cb6264/index.html?appID=72596'
        }
        resp = ss.get(url=url, headers=header, params=body).json()
        if resp['code'] == 0:
            data = resp['data']
        else:
            print('打开活动失败')
            return

        # 获取到活动页面链接
        url = data
        resp = ss.get(url=url, headers=header)
        if resp.status_code == 200:
            message('打开活动页面成功')
            # 获取token
            get_tokenkey(ss)

        else:
            print('打开活动失败')

    except Exception as e:
        print(e)


def get_tokenkey(ss):
    url = 'https://72596.activity-17.m.duiba.com.cn/projectx/p30cb6264/getTokenKey'
    tokenkey = ss.get(url=url).text
    windowh = '''
    window = {};
    
    '''
    # 玩5把
    for i in range(5):
        jstext = windowh + tokenkey + '\n'
        tokenstr = gettoken(ss)
        jstext = jstext + tokenstr
        ctx = execjs.compile(jstext)
        sign = ctx.call('ohjaiohdf')
        print('开始调用start接口')
        print(f'获取到签名:{sign}')
        # 调用开始接口
        t = time.time()
        url = 'https://72596.activity-17.m.duiba.com.cn/projectx/p30cb6264/activity/start.do'
        body = {
            'token': sign,
            'user_type': '1',
            'is_from_share': '1',
            '__ts__': int(round(t * 1000))
        }

        resp = ss.get(url=url, params=body).json()

        if resp['success']:
            startid = resp['startId']
            duration = resp['duration']
            if int(duration) > 0:
                print(f'等待~~~游戏时长:{duration}')
                time.sleep(duration)
            # 调用提交接口
            jstext = windowh + tokenkey + '\n'
            tokenstr = gettoken(ss)
            jstext = jstext + tokenstr
            ctx = execjs.compile(jstext)
            sign = ctx.call('ohjaiohdf')
            print('开始调用submit接口')
            print(f'获取到签名:{sign}')
            t = time.time()
            url = 'https://72596.activity-17.m.duiba.com.cn/projectx/p30cb6264/activity/submit.do'
            score = random.randint(1, 5)
            body = {
                'token': sign,
                'user_type': '1',
                'is_from_share': '1',
                '__ts__': int(round(t * 1000)),
                'startId': startid,
                'score': score
            }
            resp = ss.get(url=url, params=body).json()
            print(resp)
        else:
            print(f'活动开始失败:{resp["message"]}')
            break


def gettoken(ss):
    url = 'https://72596.activity-17.m.duiba.com.cn/projectx/p30cb6264/getToken'
    resp = ss.get(url=url).json()
    if resp['success']:
        data = resp['data']
        return data

    return None


if __name__ == '__main__':
    for tk in tokens:
        p = multiprocessing.Process(target=start, args=(tk,))
        p.start()

