#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
北京现代APP，签到、浏览得积分、答题得积分
"""

import os
import sys
import time
import requests
import random
from messageInfo import message, get_message_info
from shici import get_today_shi_ci

ss = requests.session()

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


today_answer = ''


def start():
    for tk in tokens:
        do_sign(tk)
        do_scan_score(tk)
        do_answer(tk)
        do_comment(tk)


def do_sign(tk):
    try:

        message("===开始签到===")
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/user/reward_list'
        header = {
            'App-Version': '7.8.3',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Token': tk,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148bjxd',
            'Connection': 'keep-alive',
            'Referer': 'https://bm2-wx.bluemembers.com.cn/app/lottery',
            'Device': 'iOS',
            'Origin-Id': 'D25BD59F-75AC-4D70-AE10-3DB6C4173858'
        }
        resp = ss.get(url=url, headers=header).json()
        print(resp)
        if resp['code'] == 0:
            hid = resp['data']['hid']
            reward_hash = resp['data']['rewardHash']
            reward_list = resp['data']['list']
            for reward in reward_list:
                if reward['hid'] == hid:
                    score = reward['score']

        url = 'https://bm2-api.bluemembers.com.cn/v1/app/user/reward_report'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'App-Version': '7.8.3',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Token': tk,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148bjxd',
            'Connection': 'keep-alive',
            'Referer': 'https://bm2-wx.bluemembers.com.cn/app/lottery',
            'Device': 'iOS',
            'Origin-Id': 'D25BD59F-75AC-4D70-AE10-3DB6C4173858',
            'Content-Type': 'application/json;charset=utf-8'
        }
        body = {
            'hid': hid,
            'hash': reward_hash
        }
        resp = ss.post(url=url, headers=header, json=body).json()
        print(resp)
        if resp['code'] == 0:
            message(f"签到成功,获取{score}积分")
        else:
            message(resp['msg'])
    except Exception as e:
        print(e)


def do_scan_score(tk):
    try:
        message("浏览得积分")
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/score'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'App-Version': '7.8.3',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Token': tk,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148bjxd',
            'Connection': 'keep-alive',
            'Referer': 'https://bm2-wx.bluemembers.com.cn/app/lottery',
            'Device': 'iOS',
            'Origin-Id': 'D25BD59F-75AC-4D70-AE10-3DB6C4173858',
            'Content-Type': 'application/json;charset=utf-8'
        }
        body = {
            'action': 12
        }
        resp = ss.post(url=url, headers=header, json=body).json()
        print(resp)
        if resp['code'] == 0 and resp['data']['is_stop']:
            message(f"浏览得积分：{resp['data']['score']}")
        else:
            message(resp['msg'])
    except Exception as e:
        print(e)


def do_comment(tk):
    try:
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/comment/create2'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'App-Version': '7.8.3',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Token': tk,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148bjxd',
            'Connection': 'keep-alive',
            'Referer': 'https://bm2-wx.bluemembers.com.cn/app/lottery',
            'Device': 'iOS',
            'Origin-Id': 'D25BD59F-75AC-4D70-AE10-3DB6C4173858',
            'Content-Type': 'application/json;charset=utf-8'
        }
        comment = get_today_shi_ci()
        comment = comment + '\n' + f'今日答案：{today_answer}'
        body = {
            'category': 4,
            'info_hid': '1f12a40e0cc6461db3aec81c8479df6e',
            'planet': '平台指南',
            'planet_hid': '7aef177228f840dca8147400dd19bd33',
            'publish_user_hid': '9d2d7a8843714f8fabae9922676fd2c8',
            'title': '在线宠粉，速来pick 精华帖攻略！',
            'topic': '精华帖攻略',
            'topic_hid': 'ead55a71c9424d9aab41990b7d096eac',
            'content': comment,
        }
        resp = ss.post(url=url, headers=header, json=body).json()
        print(resp)
        if resp['code'] == 0:
            message(f"评论成功,评论内容:【{comment}】")
        else:
            message(resp['msg'])
    except Exception as e:
        print(e)


def do_answer(tk):
    try:
        now = time.strftime("%Y%m%d", time.localtime())
        url = f'https://bm2-api.bluemembers.com.cn/v1/app/special/daily/ask_info?date={now}'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'App-Version': '7.8.3',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Token': tk,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148bjxd',
            'Connection': 'keep-alive',
            'Referer': 'https://bm2-wx.bluemembers.com.cn/app/lottery',
            'Device': 'iOS',
            'Origin-Id': 'D25BD59F-75AC-4D70-AE10-3DB6C4173858',
            'Content-Type': 'application/json;charset=utf-8'
        }
        resp = ss.get(url=url, headers=header).json()
        print(resp)
        if resp['code'] == 0:
            if resp['data']['state'] == 1:
                message("未答题，开始答题")
                url = 'https://bm2-api.bluemembers.com.cn/v1/app/special/daily/ask_answer'
                question_info = resp['data']['question_info']
                questions_hid = question_info['questions_hid']
                content = question_info['content']
                options = question_info['option']
                # 随机选择一个答题选项
                answer = random.choice(options)['option']

                # 从评论列表中识别出答案
                tmp_option_map = {
                }
                for option in options:
                    tmp_option_map[option['option']] = 0

                comment_contents = get_comment_list(tk)
                for content in comment_contents:
                    for op in tmp_option_map.keys():
                        if content.upper().find(op) >= 0:
                            tmp_option_map[op] = tmp_option_map[op] + 1

                max_count = 0
                for key, value in tmp_option_map.items():
                    if value > max_count:
                        answer = key
                        max_count = value

                global today_answer
                today_answer = answer
                body = {
                    'answer': answer,
                    'questions_hid': questions_hid
                }
                resp = ss.post(url=url, headers=header, json=body).json()
                print(resp)
                if resp['code'] == 0:
                    message(resp['data']['answer'])
                    if resp['data']['state'] == 2:
                        message("答题正确")
                        today_answer = answer
                    else:
                        message("答题错误")
                        today_answer = ''
                else:
                    message(resp['info'])
            else:
                message("已完成答题，跳过")
        else:
            message(resp['msg'])
    except Exception as e:
        print(e)


def get_comment_list(tk):
    try:
        message("获取评论列表，用于识别出今日答案")
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/white/comment/new_list?category=4&info_hid=1f12a40e0cc6461db3aec81c8479df6e&page_no=1&page_size=80'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'App-Version': '7.8.3',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Token': tk,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148bjxd',
            'Connection': 'keep-alive',
            'Referer': 'https://bm2-wx.bluemembers.com.cn/app/lottery',
            'Device': 'iOS',
            'Origin-Id': 'D25BD59F-75AC-4D70-AE10-3DB6C4173858',
            'Content-Type': 'application/json;charset=utf-8'
        }
        resp = ss.get(url=url, headers=header).json()
        print(resp)
        if resp['code'] == 0:
            c_list = resp['data']['list']
            now = time.strftime("%Y-%m-%d", time.localtime())
            contents = []
            for comment in c_list:
                if comment['created_at'].startswith(now):
                    contents.append(comment['content'])

            return contents
        else:
            return []
    except Exception as e:
        print(e)
        return []


if __name__ == '__main__':
    start()
    send('【北京现代APP签到、任务】', get_message_info())
