#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
众筹许愿池
TODO:互助未完成
"""

# ck 优先读取【JDCookies.txt】 文件内的ck  再到 ENV的 变量 JD_COOKIE='ck1&ck2' 最后才到脚本内 cookies=ck
cookies = ''

### 推送参数设置
# TG 机器人token
TG_BOT_TOKEN = ''
# TG用户id
TG_USER_ID = ''
# TG代理ip
TG_PROXY_IP = ''
# TG代理端口
TG_PROXY_PORT = ''
# TG 代理api
TG_API_HOST = ''
# 微信推送加+
PUSH_PLUS_TOKEN = ''
QYWX_AM = ''
BARK = ''

# 建议调整一下的参数
# UA 可自定义你的，注意格式: 【 jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1 】
UserAgent = ''

import os, re, sys, datetime, time
import random

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote, quote_plus
import json

requests.packages.urllib3.disable_warnings()

ss = requests.session()

pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
t = time.time()
message_info = ''
notify_mode = []
all_get_bean = 0

# 获取TG_BOT_TOKEN
if "TG_BOT_TOKEN" in os.environ:
    if len(os.environ["TG_BOT_TOKEN"]) > 1:
        TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
        print("已获取并使用Env环境 TG_BOT_TOKEN")
# 获取TG_USER_ID
if "TG_USER_ID" in os.environ:
    if len(os.environ["TG_USER_ID"]) > 1:
        TG_USER_ID = os.environ["TG_USER_ID"]
        print("已获取并使用Env环境 TG_USER_ID")
# 获取代理ip
if "TG_PROXY_IP" in os.environ:
    if len(os.environ["TG_PROXY_IP"]) > 1:
        TG_PROXY_IP = os.environ["TG_PROXY_IP"]
        print("已获取并使用Env环境 TG_PROXY_IP")
# 获取TG 代理端口
if "TG_PROXY_PORT" in os.environ:
    if len(os.environ["TG_PROXY_PORT"]) > 1:
        TG_PROXY_PORT = os.environ["TG_PROXY_PORT"]
        print("已获取并使用Env环境 TG_PROXY_PORT")
    elif not TG_PROXY_PORT:
        TG_PROXY_PORT = ''
# 获取TG TG_API_HOST
if "TG_API_HOST" in os.environ:
    if len(os.environ["TG_API_HOST"]) > 1:
        TG_API_HOST = os.environ["TG_API_HOST"]
        print("已获取并使用Env环境 TG_API_HOST")
# 获取pushplus+ PUSH_PLUS_TOKEN
if "PUSH_PLUS_TOKEN" in os.environ:
    if len(os.environ["PUSH_PLUS_TOKEN"]) > 1:
        PUSH_PLUS_TOKEN = os.environ["PUSH_PLUS_TOKEN"]
        print("已获取并使用Env环境 PUSH_PLUS_TOKEN")
# 获取企业微信应用推送 QYWX_AM
if "QYWX_AM" in os.environ:
    if len(os.environ["QYWX_AM"]) > 1:
        QYWX_AM = os.environ["QYWX_AM"]
        print("已获取并使用Env环境 QYWX_AM")
# Bark
if "BARK" in os.environ:
    if len(os.environ["BARK"]) > 1:
        BARK = os.environ["BARK"]
        print("已获取并使用Env环境 BARK")
elif "BARK_PUSH" in os.environ:
    if len(os.environ["BARK_PUSH"]) > 1:
        BARK = os.environ["BARK_PUSH"]
        print("已获取并使用Env环境 BARK_PUSH")


def nowtime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def message(str_msg):
    global message_info
    print(str_msg)
    message_info = "{}\n{}".format(message_info, str_msg)
    sys.stdout.flush()


# 获取通知，
if PUSH_PLUS_TOKEN:
    notify_mode.append('pushplus')
if TG_BOT_TOKEN and TG_USER_ID:
    notify_mode.append('telegram_bot')
if QYWX_AM:
    notify_mode.append('wecom_app')
if BARK:
    notify_mode.append('bark')


# tg通知
def telegram_bot(title, content):
    try:
        print("\n")
        bot_token = TG_BOT_TOKEN
        user_id = TG_USER_ID
        if not bot_token or not user_id:
            print("tg服务的bot_token或者user_id未设置!!\n取消推送")
            return
        print("tg服务启动")
        if TG_API_HOST:
            url = f"{TG_API_HOST}/bot{TG_BOT_TOKEN}/sendMessage"
        else:
            url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'chat_id': str(TG_USER_ID), 'text': f'{title}\n\n{content}', 'disable_web_page_preview': 'true'}
        proxies = None
        if TG_PROXY_IP and TG_PROXY_PORT:
            proxyStr = "http://{}:{}".format(TG_PROXY_IP, TG_PROXY_PORT)
            proxies = {"http": proxyStr, "https": proxyStr}
        try:
            response = requests.post(url=url, headers=headers, params=payload, proxies=proxies).json()
        except:
            print('推送失败！')
        if response['ok']:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)


# push推送
def pushplus_bot(title, content):
    try:
        print("\n")
        if not PUSH_PLUS_TOKEN:
            print("PUSHPLUS服务的token未设置!!\n取消推送")
            return
        print("PUSHPLUS服务启动")
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSH_PLUS_TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)


# BARK
def bark_push(title, content):
    print("\n")
    if not BARK:
        print("bark服务的bark_token未设置!!\n取消推送")
        return
    print("bark服务启动")
    try:
        response = requests.get('''https://api.day.app/{0}/{1}/{2}'''.format(BARK, title, quote_plus(content))).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)
        print('Bark推送失败！')


def send(title, content):
    """
    使用 bark, telegram bot, dingding bot, serverJ 发送手机推送
    :param title:
    :param content:
    :return:
    """
    content = content + "\n\n" + "仅供用于学习"
    for i in notify_mode:

        if i == 'telegram_bot':
            if TG_BOT_TOKEN and TG_USER_ID:
                telegram_bot(title=title, content=content)
            else:
                print('未启用 telegram机器人')
            continue
        elif i == 'pushplus':
            if PUSH_PLUS_TOKEN:
                pushplus_bot(title=title, content=content)
            else:
                print('未启用 PUSHPLUS机器人')
            continue
        elif i == 'wecom_app':
            if QYWX_AM:
                wecom_app(title=title, content=content)
            else:
                print('未启用企业微信应用消息推送')
            continue
        elif i == 'bark':
            if BARK:
                bark_push(title=title, content=content)
            else:
                print('未启用Bark APP应用消息推送')
            continue
        else:
            print('此类推送方式不存在')


# 企业微信 APP 推送
def wecom_app(title, content):
    try:
        if not QYWX_AM:
            print("QYWX_AM 并未设置！！\n取消推送")
            return
        QYWX_AM_AY = re.split(',', QYWX_AM)
        if 4 < len(QYWX_AM_AY) > 5:
            print("QYWX_AM 设置错误！！\n取消推送")
            return
        corpid = QYWX_AM_AY[0]
        corpsecret = QYWX_AM_AY[1]
        touser = QYWX_AM_AY[2]
        agentid = QYWX_AM_AY[3]
        try:
            media_id = QYWX_AM_AY[4]
        except:
            media_id = ''
        wx = WeCom(corpid, corpsecret, agentid)
        # 如果没有配置 media_id 默认就以 text 方式发送
        if not media_id:
            message = title + '\n\n' + content
            response = wx.send_text(message, touser)
        else:
            response = wx.send_mpnews(title, content, media_id, touser)
        if response == 'ok':
            print('推送成功！')
        else:
            print('推送失败！错误信息如下：\n', response)
    except Exception as e:
        print(e)


class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace('\n', '<br/>'),
                        "digest": message
                    }
                ]
            }
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]


def userAgent():
    global UserAgent
    """
    随机生成一个UA
    jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1
    :return: ua
    """
    if not UserAgent:
        uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
        addressid = ''.join(random.sample('1234567898647', 10))
        iosVer = ''.join(
            random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
        iosV = iosVer.replace('.', '_')
        iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
        ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
            random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
            random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
        UserAgent = f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'

    return UserAgent


class getJDCookie(object):
    # 适配各种平台环境ck
    def getckfile(self):
        if os.path.exists(pwd + 'JDCookies.txt'):
            return pwd + 'JDCookies.txt'
        elif os.path.exists('/ql/config/env.sh'):
            message("当前环境青龙面板新版")
            return '/ql/config/env.sh'
        elif os.path.exists('/ql/config/cookie.sh'):
            message("当前环境青龙面板旧版")
            return '/ql/config/env.sh'
        elif os.path.exists('/jd/config/config.sh'):
            message("当前环境V4")
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
                            message("当前获取使用 JDCookies.txt 的cookie")
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
                    message("已获取并使用Env环境 Cookie")
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
            message(context)
            send("【JD入会领豆】Cookie 已失效！", context)
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
                message("您已配置{}个账号".format(len(result)))
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
                    message("没有可用Cookie，已退出")
                    exit(3)
            else:
                message("cookie 格式错误！...本次操作已退出")
                exit(4)
        else:
            message("cookie 格式错误！...本次操作已退出")
            exit(4)


getCk = getJDCookie()
getCk.getCookie()


def get_task_list(ck):
    print("获取任务列表...")
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
            'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
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
            'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
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
                'User-Agent': 'jdapp;iPhone;10.0.6;14.1;99c79220e330f7bfeff44d53f29b7e43017dc898;network/wifi;model/iPhone10,1;addressid/138664467;appBuild/167724;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/',
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
    # send("【众筹许愿池】", message_info)


if __name__ == '__main__':
    start()
