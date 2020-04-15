#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: frequency.py
@time: 2020/04/13
"""

from .configs import FREQUENCY_UNIT_LIST


def sizeof_frequency_fmt(value, fmt=None, with_unit=True):
    """
    频率大小格式化
    :param value: 传入频率Hz数
    :param fmt: 格式换后字符串格式
    :param with_unit: 输出字符串是否带单位
    :return: 转换格式后输出字符串
    """
    for index, item in enumerate(FREQUENCY_UNIT_LIST):
        if fmt and item == fmt:
            return "%.2f%s" % (value, item) if with_unit else round(value, 2)
        if not fmt and (value < 1000.00 or index == len(FREQUENCY_UNIT_LIST) - 1):
            return "%.2f%s" % (value, item) if with_unit else round(value, 2)
        value /= 1000.00


def sizeof_frequency_parse(string):
    """
    频率大小格式化字符串解析
    :param string: 需解析字符串
    :return: 输出解析后的Hz数
    """
    for index, fmt in enumerate(FREQUENCY_UNIT_LIST):
        n = len(FREQUENCY_UNIT_LIST) - 1 - index
        if string.endswith(fmt):
            num = float(string.rstrip(fmt))
            num = num * (1000.0 ** n)
            return num
    return 0
