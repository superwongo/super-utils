#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: timezone.py
@time: 2020/04/13
"""


def timezone_convert(timestamp, fmt=None, raw_tz='UTC', tz='Asia/Shanghai'):
    """
    时区转换
    :param timestamp: 需转换时区的时间戳
    :param fmt: 转换时区后输出对应格式的字符串，若为None，则仍输出时间戳
    :param raw_tz: 原时区
    :param tz: 将要转换的时区
    :return: 转换时候后的字符串或者时间戳
    """
    try:
        from pytz import timezone
    except ImportError as e:
        raise ImportError('请安装三方库pytz')
    timestamp = timestamp.replace(tzinfo=timezone(raw_tz)).astimezone(timezone(tz))
    return timestamp.strftime(fmt) if fmt else timestamp
