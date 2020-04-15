#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: storage.py
@time: 2020/04/13
"""

from .configs import STORAGE_UNIT_LIST


def sizeof_storage_fmt(value, fmt=None, with_unit=True):
    """
    存储大小格式化
    :param value: 存储字节数
    :param fmt: 转换格式
    :param with_unit: 转换后是否携带单位
    :return: 转换单位后字符串
    """
    for index, item in enumerate(STORAGE_UNIT_LIST):
        if fmt and item == fmt:
            return "%.2f%s" % (value, item) if with_unit else round(value, 2)
        if not fmt and (value < 1024.00 or index == len(STORAGE_UNIT_LIST) - 1):
            return "%.2f%s" % (value, item) if with_unit else round(value, 2)
        value /= 1024.00


def sizeof_storage_parse(string):
    """
    存储大小格式化字符串解析
    :param string: 讯转换字符串（带单位）
    :return: 存储字节数
    """
    for index, fmt in enumerate(STORAGE_UNIT_LIST):
        if string.endswith(fmt):
            num = float(string.rstrip(fmt))
            num = num * (1024.0 ** index)
            return num
    return 0
