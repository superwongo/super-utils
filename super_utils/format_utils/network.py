#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: network.py
@time: 2020/04/13
"""

from .configs import NETWORK_UNIT_LIST


def sizeof_network_fmt(value, unit_byte=False, fmt=None, with_unit=True):
    """
    网速大小格式化
    :param value: 网络每秒bit数，若unit_byte为True，则为每秒byte数
    :param unit_byte: 传入值是否为byte数，若为字节数会转为bit数
    :param fmt: 输出字符串格式
    :param with_unit: 是否带单位输出
    :return: 输出转换后的字符串
    """
    if unit_byte:
        value = value * 8
    for index, item in enumerate(NETWORK_UNIT_LIST):
        if fmt and item == fmt:
            return "%.2f%s" % (value, item) if with_unit else round(value, 2)
        if not fmt and (value < 1000.00 or index == len(NETWORK_UNIT_LIST) - 1):
            return "%.2f%s" % (value, item) if with_unit else round(value, 2)
        value /= 1000.00


def sizeof_network_parse(string):
    """网速大小格式化字符串解析"""
    for index, fmt in enumerate(NETWORK_UNIT_LIST):
        n = len(NETWORK_UNIT_LIST) - 1 - index
        if string.endswith(fmt):
            num = float(string.rstrip(fmt))
            num = num * (1000.0 ** n)
            return num
    return 0
