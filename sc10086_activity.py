#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
四川移动APP-优享会员活动
DONE:
签到，签到开宝箱，熊掌门转转转，熊掌门邀请好友相互帮助抽奖，足球欧洲杯抽奖，优享大礼包生成及相互瓜分

TODO:熊掌门抽奖次数获取判断，足球欧洲杯任务及抽奖次数判断
"""

import os
import sys
import time

import requests
import json
import base64
import random
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

gifs = []

def start():
    message(f"一共【{len(cookies)}】个账号")
    # 先熊掌门相互助力
    for ck in cookies:
        sso_cookie = sso_cookies[cookies.index(ck)]
        for share_phone in sso_cookies:
            time.sleep(1)
            help_draw(ck, sso_cookie, share_phone)

    time.sleep(1)
    for ck in cookies:
        message(f"开始任务：第【{cookies.index(ck)+1}】个账号")
        sso_cookie = sso_cookies[cookies.index(ck)]
        # 签到
        do_sign(ck, sso_cookie)
        time.sleep(1)
        # 签到开宝箱
        sign_draw(sso_cookie)
        time.sleep(1)
        # 熊掌门转转
        xzm_draw(sso_cookie)
        time.sleep(1)
        # 足球欧洲杯抽奖
        epncup_draw(sso_cookie)
        time.sleep(1)
        share_phone, month = do_draw_gif(sso_cookie)

        # 保存大礼包信息，最后再统一相互领取大礼包
        gifs.append(
            {
                'share_phone': share_phone,
                'month': month
            }
        )
        print(gifs)

    # 相互抽取优享大礼包，瓜分流量
    for ck in cookies:
        sso_cookie = sso_cookies[cookies.index(ck)]
        draw_gif_ticket(ck, sso_cookie)


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
    print(resp)
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
    print(resp)
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
            print(resp)
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


def epncup_draw(sso_cookie):
    print("足球欧洲杯抽奖")
    url = 'https://wap.sc.10086.cn/scmccCampaign/epncup/doDraw.do'
    body = {
        'SSOCookie': sso_cookie,
        'canals': 'zt1'
    }
    resp = ss.post(url=url, data=body).json()
    print(resp)
    if resp['result']['code'] == 0:
        message("足球欧洲杯抽奖，中奖了")
        message(f"{resp['result']['obj']['name']}")
    else:
        message(f"{resp['result']['info']}")


def help_draw(ck, sso_cookie, share_phone):
    print("熊掌门助力好友抽奖")
    url = 'https://wap.sc.10086.cn/scmccCampaign/dzp2020help/helpDraw.do'
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
        'SSOCookie': sso_cookie,
        'canals': 'zt1',
        'sharePhone': share_phone
    }
    resp = ss.post(url=url, headers=header, data=body).json()
    print(resp)
    if resp['result']['code'] == 0:
        message(f"{resp['result']['info']}")
        message(f"{resp['result']['obj']}")
    else:
        message(f"{resp['result']['info']}")


def do_draw_gif(sso_cookie):
    message("初始化生成优享礼包，分享出去共同瓜分流量")
    url = 'https://wap.sc.10086.cn/scmccCampaign/oneVipGift/doDrawGift.do'
    body = {
        'SSOCookie': sso_cookie
    }
    resp = ss.post(url=url, data=body).json()
    print(resp)
    month = resp['result']['obj']['month']
    share_phone = resp['result']['obj']['sharePhone']
    jump_url = f"https://wap.sc.10086.cn/scmccCampaign/oneVipV2/index.html?channel=ztapp&SSOCookie={sso_cookie}"
    bytes_url = jump_url.encode("utf-8")
    share_url = f"http://wap.sc.10086.cn/scmccCampaign/oneVip/share.html?s={share_phone}&m={month}&jumpUrl={base64.b64encode(bytes_url).decode()}"
    message(f"生成大礼包url成功")
    message(share_url)
    return share_phone, month


def draw_gif_ticket(ck, sso_cookie):
    for dic in gifs:
        time.sleep(1)
        share_phone = dic['share_phone']
        month = dic['month']
        message(f"【{sso_cookie}】抽取大礼包,sharePhone:{share_phone}, month:{month}")
        key = ''.join(str(random.choice(range(1, 10))) for _ in range(16))
        url = f"http://wap.sc.10086.cn/scmccCampaign/oneVipGift/drawGiftTicket.do?key=0.{key}"
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
            'SSOCookie': sso_cookie,
            's': share_phone,
            'm': month
        }
        resp = ss.post(url=url, headers=header, data=body).json()
        print(resp)


if __name__ == '__main__':
    start()
    send("【移动优享会员活动】", get_message_info())
