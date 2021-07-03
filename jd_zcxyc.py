#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
众筹许愿池
TODO:互助未完成
"""

cookies = ''

# 建议调整一下的参数
# UA 可自定义你的，注意格式
UserAgent = 'jdappiPhone10.0.413.7ca6eb91a888be488f194b9d9216cf711dd1b221anetwork/wifiADID/8679C062-A41A-4A25-88F1-50A7A3EEF34Amodel/iPhone8,1addressid/3723896896appBuild/167707jdSupportDarkMode/0Mozilla/5.0 (iPhone CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148supportJDSHWK/1'

import os, re
import random, string

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote, quote
import json
import time

requests.packages.urllib3.disable_warnings()

ss = requests.session()

pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
t = time.time()


class getJDCookie(object):
    # 适配各种平台环境ck
    def getckfile(self):
        if os.path.exists(pwd + 'JDCookies.txt'):
            return pwd + 'JDCookies.txt'
        elif os.path.exists('/ql/config/env.sh'):
            print("当前环境青龙面板新版")
            return '/ql/config/env.sh'
        elif os.path.exists('/ql/config/cookie.sh'):
            print("当前环境青龙面板旧版")
            return '/ql/config/env.sh'
        elif os.path.exists('/jd/config/config.sh'):
            print("当前环境V4")
            return '/jd/config/config.sh'
        elif os.path.exists(pwd + 'JDCookies.txt'):
            return pwd + 'JDCookies.txt'
        return pwd + 'JDCookies.txt'

    # 获取cookie
    def getCookie(self):
        global cookies
        ckfile = self.getckfile()
        try:
            if os.path.exists(ckfile):
                with open(ckfile, "r", encoding="utf-8") as f:
                    cks = f.read()
                    f.close()
                if 'pt_key=' in cks and 'pt_pin=' in cks:
                    r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
                    cks = r.findall(cks)
                    if len(cks) > 0:
                        if 'JDCookies.txt' in ckfile:
                            print("当前获取使用 JDCookies.txt 的cookie")
                        cookies = ''
                        for i in cks:
                            cookies += i
                        return
            else:
                with open(pwd + 'JDCookies.txt', "w", encoding="utf-8") as f:
                    cks = "#多账号换行，以下示例：（通过正则获取此文件的ck，理论上可以自定义名字标记ck，也可以随意摆放ck）\n账号1【Curtinlv】cookie1;\n账号2【TopStyle】cookie2;"
                    f.write(cks)
                    f.close()
            if "JD_COOKIE" in os.environ:
                if len(os.environ["JD_COOKIE"]) > 10:
                    cookies = os.environ["JD_COOKIE"]
                    print("已获取并使用Env环境 Cookie")
        except Exception as e:
            print(f"【getCookie Error】{e}")

    # 检测cookie格式是否正确
    def getUserInfo(self, ck, pinName, userNum):
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback=GetJDUserInfoUnion'
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'close',
            'Referer': 'https://home.m.jd.com/myJd/home.action',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'me-api.jd.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'zh-cn'
        }
        try:
            resp = requests.get(url=url, verify=False, headers=headers, timeout=60).text
            r = re.compile(r'GetJDUserInfoUnion.*?\((.*?)\)')
            result = r.findall(resp)
            userInfo = json.loads(result[0])
            nickname = userInfo['data']['userInfo']['baseInfo']['nickname']
            return ck, nickname
        except Exception:
            context = f"账号{userNum}【{pinName}】Cookie 已失效！请重新获取。"
            print(context)
            return ck, False

    def iscookie(self):
        """
        :return: cookiesList,userNameList,pinNameList
        """
        cookiesList = []
        userNameList = []
        pinNameList = []
        if 'pt_key=' in cookies and 'pt_pin=' in cookies:
            r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
            result = r.findall(cookies)
            if len(result) >= 1:
                print("您已配置{}个账号".format(len(result)))
                u = 1
                for i in result:
                    r = re.compile(r"pt_pin=(.*?);")
                    pinName = r.findall(i)
                    pinName = unquote(pinName[0])
                    # 获取账号名
                    ck, nickname = self.getUserInfo(i, pinName, u)
                    if nickname != False:
                        cookiesList.append(ck)
                        userNameList.append(nickname)
                        pinNameList.append(pinName)
                    else:
                        u += 1
                        continue
                    u += 1
                if len(cookiesList) > 0 and len(userNameList) > 0:
                    return cookiesList, userNameList, pinNameList
                else:
                    print("没有可用Cookie，已退出")
                    exit(3)
            else:
                print("cookie 格式错误！...本次操作已退出")
                exit(4)
        else:
            print("cookie 格式错误！...本次操作已退出")
            exit(4)


getCk = getJDCookie()
getCk.getCookie()


def get_task_list(ck):
    url = 'https://api.m.jd.com/client.action?functionId=healthyDay_getHomeData&body={"appId":"1EFVQwQ","taskToken":"","channelId":1}&client=wh5&clientVersion=1.0.0'
    header = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
        'Accept-Language': 'zh-cn',
        'Host': 'api.m.jd.com'
    }
    resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
    return resp['data']['result']['taskVos']


def do_task(task, ck):
    task_type = task['taskType']
    taskid = task['taskId']
    if int(task_type) == 26:
        '''关注众筹频道'''
        arr = task['shoppingActivityVos']
        for tt in arr:
            guanzhu(tt, taskid, ck)
    elif int(task_type) == 9:
        '''浏览众筹频道'''
        arr = task['shoppingActivityVos']
        wait_duration = task['waitDuration']
        for tt in arr:
            liulan(tt, taskid, wait_duration, ck)
    elif int(task_type) == 8:
        '''浏览任务'''
        arr = task['productInfoVos']
        wait_duration = task['waitDuration']
        for tt in arr:
            liulan_sku(tt, taskid, wait_duration, ck)
    elif int(task_type) == 1:
        '''关注任务'''
        arr = task['followShopVo']
        for tt in arr:
            guanzhu_shop(tt, taskid, ck)
    elif int(task_type) == 13:
        '''签到'''
        qd = task['simpleRecordInfoVo']
        qiandao(qd, taskid, ck)


def guanzhu(task, taskId, ck):
    print(f"开始做任务：{task['title']}")
    url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
          task['taskToken'] + '","taskId":' + str(taskId) + ',"actionType":0}&client=wh5&clientVersion=1.0.0'
    header = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
        'Accept-Language': 'zh-cn',
        'Host': 'api.m.jd.com'
    }
    resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
    print(resp['data']['bizMsg'])


def liulan(task, taskid, duration, ck):
    print(f"开始做任务：{task['title']}")
    '''领取任务'''
    url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
          task['taskToken'] + '","taskId":' + str(taskid) + ',"actionType":1}&client=wh5&clientVersion=1.0.0'
    header = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
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
            'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
            'Accept-Language': 'zh-cn',
            'Host': 'api.m.jd.com'
        }
        resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
        print(resp['data']['bizMsg'])


def liulan_sku(task, taskid, duration, ck):
    print(f"开始做浏览任务：{task['skuName']}")
    '''领取任务'''
    url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
          task['taskToken'] + '","taskId":' + str(taskid) + ',"actionType":1}&client=wh5&clientVersion=1.0.0'
    header = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
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
            'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
            'Accept-Language': 'zh-cn',
            'Host': 'api.m.jd.com'
        }
        resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
        print(resp['data']['bizMsg'])


def guanzhu_shop(task, taskId, ck):
    print(f"开始做关注店铺任务：{task['shopName']}")
    url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
          task['taskToken'] + '","taskId":' + str(taskId) + ',"actionType":0}&client=wh5&clientVersion=1.0.0'
    header = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
        'Accept-Language': 'zh-cn',
        'Host': 'api.m.jd.com'
    }
    resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
    print(resp['data']['bizMsg'])


def qiandao(task, taskId, ck):
    print("开始签到")
    url = 'https://api.m.jd.com/client.action?functionId=harmony_collectScore&body={"appId":"1EFVQwQ","taskToken":"' + \
          task['taskToken'] + '","taskId":' + str(taskId) + ',"actionType":0}&client=wh5&clientVersion=1.0.0'
    header = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
        'Accept-Language': 'zh-cn',
        'Host': 'api.m.jd.com'
    }
    resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
    print(resp['data']['bizMsg'])


def choujiang(ck):
    print("开始抽奖")
    bl = True
    while bl:
        url = 'https://api.m.jd.com/client.action?functionId=interact_template_getLotteryResult&body={"appId":"1EFVQwQ"}&client=wh5&clientVersion=1.0.0'
        header = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/UQwNm9fNDey3xNEUTSgpYikqnXR/index.html?lng=104.125467&lat=30.685642&sid=d01c82020697fd64deb79524cf5dd4dw&un_area=22_1930_50948_57085',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
            'Accept-Language': 'zh-cn',
            'Host': 'api.m.jd.com'
        }
        resp = requests.get(url=url, headers=header, verify=False, timeout=30).json()
        print(resp['data']['bizMsg'])
        if int(resp['data']['bizCode']) != 0:
            bl = False


def start():
    print("### 众筹许愿池 ###")
    global cookiesList, userNameList, pinNameList
    cookiesList, userNameList, pinNameList = getCk.iscookie()
    for ck in cookiesList:
        tasks = get_task_list(ck)
        for task in tasks:
            do_task(task, ck)
        choujiang(ck)
    print("运行结束")


if __name__ == '__main__':
    start()
