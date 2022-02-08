#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""

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


def start():
    message(f"一共【{len(cookies)}】个账号")
    # 先熊掌门相互助力
    message("====熊掌门邀请好友相互助力===")
    for ck in cookies:
        message(f"账号【{cookies.index(ck) + 1}】给其他账号助力")
        sso_cookie = sso_cookies[cookies.index(ck)]
        for share_phone in sso_cookies:
            time.sleep(1)
            help_draw(ck, sso_cookie, share_phone)

    time.sleep(1)
    for ck in cookies:
        message(f"===账号【{cookies.index(ck) + 1}】开始做任务===")
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
        do_draw_gif(sso_cookie)
        time.sleep(1)
        # 足球欧洲杯抽奖
        # epncup_draw(sso_cookie)
        # time.sleep(1)
        # 会员日抽奖
        do_members_day(sso_cookie)
        # 激活卡券
        do_active_kaquan(sso_cookie)


def do_sign(ck, sso_cookie):
    try:
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
    except Exception as e:
        print(e)


def sign_draw(sso_cookie):
    try:
        print('获取宝箱信息')
        url = 'https://wap.sc.10086.cn/scmccCampaign/signCalendar/initDataV5.do'
        body = {
            'SSOCookie': sso_cookie
        }
        resp = ss.post(url=url, data=body).json()
        print(resp)
        result = resp['result']
        if result['code'] == 0:
            print('获取宝箱信息成功')
            draw_infos = json.loads(result['obj']['drawInfos'])
        else:
            print('获取宝箱信息失败')
            return

        message('===开始开宝箱===')
        for info in draw_infos:
            if info['IS_SIGN_FLAG'] == 'Y-DRAWING' and info['IS_DRAW'] == 'N':
                time.sleep(5)
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
                else:
                    message(f"开宝箱失败,{result['info']}")

        message('开宝箱完成')
    except Exception as e:
        print(e)


def xzm_draw(sso_cookie):
    try:

        message("===熊掌门转转转===")
        url = 'https://wap.sc.10086.cn/scmccCampaign/dzp2020/init.do'
        body = {
            'SSOCookie': sso_cookie,
            'canals': 'zt1'
        }
        resp = ss.post(url=url, data=body).json()
        print(resp)
        countlist = resp['result']['obj']['countlist']
        count = 0
        for dic in countlist:
            count = count + dic['count']
        print(f"一共{count}次抽奖机会")

        if count <= 0:
            return

        for i in range(count):
            time.sleep(10)
            print(f"开始第{i + 1}次抽奖")
            url = 'https://wap.sc.10086.cn/scmccCampaign/dzp2020/Draw.do'
            body = {
                'SSOCookie': sso_cookie,
                'canals': 'zt1'
            }
            resp = ss.post(url=url, data=body).json()
            print(resp)
    except Exception as e:
        print(e)


def epncup_draw(sso_cookie):
    try:
        message("===足球欧洲杯抽奖===")
        url = 'https://wap.sc.10086.cn/scmccCampaign/epncup/initPage.do'
        body = {
            'SSOCookie': sso_cookie
        }
        resp = ss.post(url=url, data=body).json()
        print(resp)
        count = 0
        if resp['result']['code'] == 0:
            user_cnt = resp['result']['obj']['userCnt']
            task_id = user_cnt['taskid'].split(',')
            complete_task = user_cnt['completeTaskId'].split(',')
            count = user_cnt['count']
        else:
            print(resp['result']['info'])

        for task in task_id:
            if complete_task.count(task) > 0:
                continue
            time.sleep(10)
            print(f"开始做任务:【{task}】")
            url = 'https://wap.sc.10086.cn/scmccCampaign/epncup/reportTask.do'
            body = {
                'SSOCookie': sso_cookie,
                'canals': 'zt1',
                'taskId': task
            }
            resp = ss.post(url=url, data=body).json()
            print(resp)
            message(resp['result']['info'])
            if resp['result']['code'] == 0:
                count = count + 1

        if count <= 0:
            return

        for i in range(count):
            time.sleep(1)
            print(f"开始第{i + 1}次抽奖")
            url = 'https://wap.sc.10086.cn/scmccCampaign/epncup/doDraw.do'
            body = {
                'SSOCookie': sso_cookie,
                'canals': 'zt1'
            }
            resp = ss.post(url=url, data=body).json()
            print(resp)
            if resp['result']['code'] == 0:
                message(f"{resp['result']['obj']['name']}")
            else:
                message(f"{resp['result']['info']}")
    except Exception as e:
        print(e)


def help_draw(ck, sso_cookie, share_phone):
    try:
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
        else:
            message(f"{resp['result']['info']}")
    except Exception as e:
        print(e)


def do_draw_gif(sso_cookie):
    try:
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
        print(share_url)
        if resp['result']['code'] == 0:
            print("开始瓜分自己生成的优享礼包")
            draw_gif_ticket(sso_cookie, share_phone, month)
        else:
            message(resp['result']['info'])
    except Exception as e:
        print(e)


def draw_gif_ticket(sso_cookie, share_phone, month):
    try:
        key = ''.join(str(random.choice(range(1, 10))) for _ in range(16))
        url = f"http://wap.sc.10086.cn/scmccCampaign/oneVipGift/drawGiftTicket.do?key=0.{key}"
        body = {
            'SSOCookie': sso_cookie,
            's': share_phone,
            'm': month
        }
        resp = ss.post(url=url, data=body).json()
        print(resp)
    except Exception as e:
        print(e)


def do_active_kaquan(sso_cookie):
    try:
        message("查询卡券列表")
        url = 'https://wap.sc.10086.cn/scmccClient/fusionCardCoupons.do'
        body = {
            'SSOCookie': sso_cookie,
            'type': 2
        }
        resp = ss.post(url=url, data=body).text
        result = base64.b64decode(resp)
        result = json.loads(result.decode())
        print(result)
        kq_list = result['retObj']['ZTList']
        if len(kq_list) <= 0:
            message("无可激活的卡券")
        for kq in kq_list:
            message(f"开始兑换{kq['cardName']},{kq['cardAmount']}")
            time.sleep(5)
            url = 'https://wap.sc.10086.cn/scmccClient/fusionCardCoupons.do'
            body = {
                'type': 1,
                'SSOCookie': sso_cookie,
                'parms': json.dumps(kq)
            }
            resp = ss.post(url=url, data=body).json()
            print(resp)
    except Exception as e:
        print(e)


def do_members_day(sso_cookie):
    try:
        message('查询会员日抽奖信息')
        key = ''.join(str(random.choice(range(1, 10))) for _ in range(16))
        url = f'https://wap.sc.10086.cn/scmccCampaign/membersDay/init.do?key=0.{key}'
        body = {
            'SSOCookie': sso_cookie
        }
        resp = ss.post(url=url, data=body).json()
        print(resp)
        if resp['result']['code'] == 0:
            obj = resp['result']['obj']
            # 报名
            is_appointment_day = obj['isAppointmentDay']
            is_appointment = obj['isAppointment']
            if is_appointment_day is True and is_appointment is False:
                url = 'https://wap.sc.10086.cn/scmccCampaign/membersDay/appointment.do'
                body = {
                    'SSOCookie': sso_cookie,
                    'channel': 'ztapp'
                }
                resp = ss.post(url=url, data=body).json()
                print(resp)
                message(resp['result']['info'])

            is_draw_prize_day = obj['isDrawPrizeDay']
            is_prize = obj['isPrize']
            if is_draw_prize_day is True and is_prize is False:
                url = 'https://wap.sc.10086.cn/scmccCampaign/membersDay/doPrize.do'
                body = {
                    'SSOCookie': sso_cookie,
                    'channel': 'ztapp'
                }
                resp = ss.post(url=url, data=body).json()
                print(resp)
                message(resp['result']['info'])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start()
    send("【移动优享会员活动】", get_message_info())
