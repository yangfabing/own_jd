# -*- coding: utf-8 -*-

import os
import sys
import datetime
import json
import requests
import akshare as ak
from trading_day import is_trading_day

authorization = None
databases_id = None

if "notion_authorization" in os.environ and os.environ["notion_authorization"]:
    authorization = os.environ['notion_authorization']
if "notion_databases_id" in os.environ and os.environ["notion_databases_id"]:
    databases_id = os.environ['notion_databases_id']

# 获取通知模块
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
if os.path.exists(cur_path + "/sendNotify.py"):
    from sendNotify import send
else:
    def send(title, content):
        pass


if authorization is None or databases_id is None:
    send('基金盯盘', 'notion authorization or databases_id 不能为空')


def get_all_fund_estimation():
    """通过 akshare 获取所有基金(天天基金)的估值
    返回值类型 pandas
    """
    fund_em_value_estimation_df = ak.fund_em_value_estimation()
    return fund_em_value_estimation_df


def get_accounts():
    """通过 Notion API 获取指定 database 里的数据"""
    headers = {
        'Authorization': authorization,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
    }

    _data = '{ "filter": { "or": [ { "property": "Status", "select": { "equals": "启用" } } ] } }'.encode()

    response = requests.post(
        f'https://api.notion.com/v1/databases/{databases_id}/query',
        headers=headers, data=_data)
    content = json.loads(response.content)
    accounts = {}
    for result in content['results']:
        accounts[result['properties']['Name']['title'][0]['plain_text']] = {
            "databases_id": result['properties']['databases_id']['rich_text'][0]['plain_text'],
            "authorization": result['properties']['authorization']['rich_text'][0]['plain_text'],
            "bark_token": result['properties']['bark_token']['rich_text'][0]['plain_text']
        }

    return accounts


def get_data(authorization, databases_id):
    """通过 Notion API 获取指定 database 里的数据"""
    headers = {
        'Authorization': authorization,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
    }

    _data = '{ "filter": { "or": [ { "property": "Status", "select": { "equals": "启用" } } ] } }'.encode()

    response = requests.post(
        f'https://api.notion.com/v1/databases/{databases_id}/query',
        headers=headers, data=_data)
    content = json.loads(response.content)
    data = {}
    for result in content['results']:
        data[result['properties']['Code']['rich_text'][0]['plain_text']] = {
            "name": result['properties']['Name']['title'][0]['plain_text'],
            "cordon": result['properties']['Decline']['select']['name'],
            "rise": result['properties']['Rise']['select']['name'],
            "communication": ""
        }

    return data


async def task(code=None, percent="", content=None, bark_token=None):
    """处理盯盘任务"""
    if content is None:
        return None

    if "-" not in percent:
        # 上涨的
        percent = percent.replace("+", '').replace("%", '')
        rise = content.get('rise')
        if not rise:
            return None

        if percent < rise:  # 不需要发通知
            return None

        message = f"基金盯盘: {content.get('name')} 今日涨幅超过 {rise}% 警戒线, 当前涨幅 {percent}% , 基金代码 {code} ."
        send('基金盯盘', message)
    else:
        # 下跌的
        percent = percent.replace("-", '').replace("%", '')
        cordon = content.get('cordon')
        if percent < cordon:  # 不需要发通知
            return None

        message = f"基金盯盘: {content.get('name')} 今日跌幅超过 {cordon}% 警戒线, 当前跌幅 {percent}% , 基金代码 {code} ."
        send('基金盯盘', message)

    return code


async def pegging():
    """主函数"""
    # 如果不是交易日，则直接结束
    if not is_trading_day():
        print(f"日期：{datetime.date.today()}，当前不是交易日")
        return

    try:
        df = get_all_fund_estimation()
    except:  # 重试
        df = get_all_fund_estimation()

    accounts = get_accounts()
    for account_name in accounts.keys():
        info = accounts.get(account_name)
        fund_data = get_data(authorization=info['authorization'], databases_id=info['databases_id'])
        code_list = fund_data.keys()
        funds = df[df['基金代码'].isin(code_list)].iloc[:, [1, 4]]
        results = []
        for _, row in funds.iterrows():
            code = row[0]
            results.append(await task(code=code, percent=row[1], content=fund_data[code],
                                      bark_token=info['bark_token']))  # 编码，涨跌幅，警戒线,消息推送token

        results = list(filter(None, results))  # 过滤是 None 的数据
        if results:
            print(f"日期：{datetime.date.today()}，账号：{account_name}，报警的监控条数{len(results)}")
        else:
            print(f"日期：{datetime.date.today()}，账号：{account_name}，没有需要报警的监控")


if __name__ == '__main__':
    # get_data()

    import asyncio

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(pegging())
    loop.close()
