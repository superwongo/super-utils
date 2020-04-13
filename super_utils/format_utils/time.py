#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: time.py
@time: 2020/04/13
"""

from .configs import TIME_UNIT_LIST


def sizeof_time_fmt(value):
    """时间大小格式化"""
    for index, item in enumerate(TIME_UNIT_LIST):
        if value < 60.00:
            return "%.2f%s" % (value, item)
        if index < len(TIME_UNIT_LIST) - 1:
            value /= 60.00
        elif value < 24.00:
            return "%.2f%s" % (value, item)
        else:
            return "%.2f%s" % (value / 24.00, '天')
