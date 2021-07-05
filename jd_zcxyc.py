#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
众筹许愿池
TODO:互助未完成
"""

import os
import sys
import time

import requests

from jdCookie import getCk
from messageInfo import message, get_message_info
from userAgent import userAgent

requests.packages.urllib3.disable_warnings()

ss = requests.session()

pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
t = time.time()
all_get_bean = 0

# 获取通知模块
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
if os.path.exists(cur_path + "/sendNotify.py"):
    from sendNotify import send
else:
    def send(title, content):
        pass
###################


def get_task_list(ck):
    print("获取任务列表...")
    url = 'https://api.m.jd.com/client.action?functionId=healthyDay_getHomeData&body={"appId":"1EFVQwQ","taskToken":"","channelId":1}&client=wh5&clientVersion=1.0.0'
    header = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-cn',
        'Host': 'api.m.jd.com'
    }
    resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
    try:
        return resp['data']['result']['taskVos']
    except Exception as e:
        message("任务列表数据获取异常")
        return {}


def do_task(group, ck):
    try:
        task_type = int(group['taskType'])
        taskid = group['taskId']
        wait_duration = group['waitDuration']
        if task_type == 26:
            '''关注众筹频道'''
            arr = group['shoppingActivityVos']
            for tt in arr:
                print(f"开始做任务：{tt['title']}")
                collect(tt, taskid, ck)
        elif task_type == 9:
            '''浏览众筹频道'''
            arr = group['shoppingActivityVos']
            for tt in arr:
                print(f"开始做任务：{tt['title']}")
                browse_task(tt, taskid, wait_duration, ck)
        elif task_type == 8:
            '''浏览任务'''
            arr = group['productInfoVos']
            for tt in arr:
                print(f"开始做浏览任务：{tt['skuName']}")
                browse_task(tt, taskid, wait_duration, ck)
        elif task_type == 1:
            '''关注任务'''
            arr = group['followShopVo']
            for tt in arr:
                print(f"开始做关注店铺任务：{tt['shopName']}")
                collect(tt, taskid, ck)
        elif task_type == 13:
            '''签到'''
            qd = group['simpleRecordInfoVo']
            signin(qd, taskid, ck)
    except Exception as e:
        print(e)


def collect(task, taskId, ck):
    try:
        url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
              task['taskToken'] + '","taskId":' + str(taskId) + ',"actionType":0}&client=wh5&clientVersion=1.0.0'
        header = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-cn',
            'Host': 'api.m.jd.com'
        }
        resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
        print(resp['data']['bizMsg'])
    except Exception as e:
        print(e)


def browse_task(task, taskid, duration, ck):
    try:
        '''领取任务'''
        url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
              task['taskToken'] + '","taskId":' + str(taskid) + ',"actionType":1}&client=wh5&clientVersion=1.0.0'
        header = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-cn',
            'Host': 'api.m.jd.com'
        }
        resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
        if int(resp['code'] == 0):
            print(resp['data']['bizMsg'])
            if int(resp['data']['bizCode']) != 1:
                return
            print(f'等待{duration}秒')
            time.sleep(duration)
            '''完成任务'''
            url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
                  task['taskToken'] + '","taskId":' + str(taskid) + ',"actionType":0}&client=wh5&clientVersion=1.0.0'
            header = {
                'Cookie': ck,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
                'Accept-Encoding': 'gzip, deflate, br',
                'User-Agent': userAgent(),
                'Accept-Language': 'zh-cn',
                'Host': 'api.m.jd.com'
            }
            resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
            print(resp['data']['bizMsg'])
    except Exception as e:
        print(e)


def signin(task, taskId, ck):
    try:
        print("开始签到")
        url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
              task['taskToken'] + '","taskId":' + str(taskId) + ',"actionType":0}&client=wh5&clientVersion=1.0.0'
        header = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-cn',
            'Host': 'api.m.jd.com'
        }
        resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
        print(resp['data']['bizMsg'])
    except Exception as e:
        print(e)


def lottery(ck):
    print("开始抽奖")
    try:
        bl = True
        while bl:
            url = 'https://api.m.jd.com/client.action?functionId=interact_template_getLotteryResult&body={"appId":"1EFVQwQ"}&client=wh5&clientVersion=1.0.0'
            header = {
                'Cookie': ck,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
                'Accept-Encoding': 'gzip, deflate, br',
                'User-Agent': userAgent(),
                'Accept-Language': 'zh-cn',
                'Host': 'api.m.jd.com'
            }
            resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
            print(resp['data']['bizMsg'])
            if int(resp['data']['bizCode']) != 0:
                bl = False
    except Exception as e:
        print(e)


def start():
    print("### 众筹许愿池 ###")
    starttime = time.perf_counter()  # 记录时间开始
    global cookiesList, userNameList, pinNameList
    cookiesList, userNameList, pinNameList = getCk.iscookie()
    for ck in cookiesList:
        message(f"账号：{userNameList[cookiesList.index(ck)]}")
        total_tasks = get_task_list(ck)
        for group in total_tasks:
            do_task(group, ck)
        lottery(ck)

    message(f"\n本次总累计获得：xxxx 京豆，请去奖品列表查看是否有实物奖品")
    endtime = time.perf_counter()  # 记录时间结束
    message("\n------- 总耗时 : %.03f 秒 seconds -------" % (endtime - starttime))
    send("【众筹许愿池】", get_message_info())


if __name__ == '__main__':
    start()
