#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
四川移动APP-优享会员活动
"""

import os
import sys
import time

import requests
import json
from messageInfo import message, get_message_info

ss = requests.session()

cookies = []
sso_cookies = []
SC_COOKIES = ''
SSOCookies = ''
if "SC_COOKIES" in os.environ and os.environ["SC_COOKIES"]:
    SC_COOKIES = os.environ['SC_COOKIES']
if "SSOCookies" in os.environ and os.environ["SSOCookies"]:
    SSOCookies = os.environ['SSOCookies']

if SC_COOKIES:
    cookies = SC_COOKIES.split('&')
if SSOCookies:
    sso_cookies = SSOCookies.split('&')


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
    message(f"一共【{len(cookies)}】个账号")
    for ck in cookies:
        message(f"开始任务：第【{cookies.index(ck)+1}】个账号")
        sso_cookie = sso_cookies[cookies.index(ck)]
        do_sign(ck, sso_cookie)
        time.sleep(1)
        sign_draw(sso_cookie)
        time.sleep(1)
        xzm_draw(sso_cookie)


def do_sign(ck, sso_cookie):
    message("开始签到...")
    url = 'https://wap.sc.10086.cn/scmccCampaign/signCalendar/sign.do'
    header = {
        'XMLHttpRequest': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/4.4.2 scmcc.mobile',
        'Connection': 'keep-alive',
        'Cookie': ck
    }
    body = {
        'SSOCookie': sso_cookie
    }
    resp = ss.post(url=url, headers=header, data=body).json()
    result = resp['result']
    message(resp)
    if result['code'] == 0:
        message("签到成功")
    else:
        message(f"签到失败，{result['info']}")


def sign_draw(sso_cookie):
    message('获取宝箱信息')
    url = 'https://wap.sc.10086.cn/scmccCampaign/signCalendar/initDataV5.do'
    body = {
        'SSOCookie': sso_cookie
    }
    resp = ss.post(url=url, data=body).json()
    message(resp)
    result = resp['result']
    if result['code'] == 0:
        message('获取宝箱信息成功')
        draw_infos = json.loads(result['obj']['drawInfos'])
    else:
        message('获取宝箱信息失败')
        return

    message('开始开宝箱...')
    for info in draw_infos:
        if info['IS_SIGN_FLAG'] == 'Y-DRAWING' and info['IS_DRAW'] == 'N':
            f_type = info['F_TYPE']
            url = 'https://wap.sc.10086.cn/scmccCampaign/signCalendar/drawNew.do'
            body = {
                'SSOCookie': sso_cookie,
                'type': f_type
            }
            resp = ss.post(url=url, data=body).json()
            message(resp)
            result = resp['result']
            if result['code'] == 0:
                message("开宝箱成功")
                obj = result['obj']
            else:
                message(f"开宝箱失败,{result['info']}")
            time.sleep(1)

    message('开宝箱完成')


def xzm_draw(sso_cookie):
    print("开始熊掌门转转转...")
    url = 'https://wap.sc.10086.cn/scmccCampaign/dzp2020/Draw.do'
    body = {
        'SSOCookie': sso_cookie,
        'canals': 'zt1'
    }
    resp = ss.post(url=url, data=body).json()
    message(resp)


if __name__ == '__main__':
    start()
    send("【移动优享会员活动】", get_message_info())
