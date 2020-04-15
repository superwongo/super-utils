#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: configs.py
@time: 2020/04/13
"""

import os
import sys

# -----日志模块相关参数----- #
current_dir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

# LOG日志存放目录
LOG_PATH = os.path.join(BASE_DIR, 'logs') \
    if sys.platform == 'win32' else os.path.join('/var/log', 'super-utils')

# 日志类型
LOG_TYPE = 'common_logger'
# 错误日志文件名称
LOG_PATH_ERROR = os.path.join(LOG_PATH, 'super_utils_error.log')
# 正常文件日志名称
LOG_PATH_INFO = os.path.join(LOG_PATH, 'super_utils_info.log')
# 日志文件最大大小，10M
LOG_FILE_MAX_BYTES = 10 * 1024 * 1024
# 日志文件轮转数量是 10 个
LOG_FILE_BACKUP_COUNT = 10
# 日志级别
LOG_LEVEL = 'INFO'
# ------------------------- #
