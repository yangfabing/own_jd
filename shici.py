#!/usr/bin/env python3
# -*- coding: utf-8 -*

import requests


def get_today_shi_ci():
    try:
        url = 'https://v1.jinrishici.com/all.json'
        resp = requests.get(url).json()
        print(resp)
        return resp['content']
    except Exception as e:
        print(e)
        return ""


if __name__ == '__main__':
    get_today_shi_ci()
