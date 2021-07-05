#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys

message_info = ''''''


def message(str_msg):
    global message_info
    print(str_msg)
    message_info = "{}\n{}".format(message_info, str_msg)
    sys.stdout.flush()


def get_message_info():
    return message_info
