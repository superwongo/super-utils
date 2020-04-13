#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: logs.py
@time: 2020/04/13
"""

import os
import logging
from logging.config import dictConfig

from .configs import LOG_FILE_MAX_BYTES, LOG_FILE_BACKUP_COUNT, LOG_PATH_ERROR, LOG_PATH_INFO, \
    LOG_TYPE, LOG_PATH, LOG_LEVEL


class LoggerGenerator(object):
    """日志对象生成器"""
    def __init__(self, log_type=LOG_TYPE, log_level=LOG_LEVEL, multiprocess=False):
        self.log_type = log_type
        self.log_level = log_level
        self.multiprocess = multiprocess
        self._logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
                },
                'verbose_info': {
                    'format': '[%(asctime)s] %(levelname)s %(process)d %(module)s line%(lineno)s: | %(message)s'
                },
                'verbose_error': {
                    'format': '[%(asctime)s] %(levelname)s %(process)d %(pathname)s line%(lineno)s: | %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'verbose_info',
                    'stream': 'ext://sys.stdout'
                },
                'info_file_handler': {
                    'class': 'cloghandler.ConcurrentRotatingFileHandler' if self.multiprocess else 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'verbose_info',
                    'filename': LOG_PATH_INFO,
                    'maxBytes': int(LOG_FILE_MAX_BYTES),
                    'backupCount': int(LOG_FILE_BACKUP_COUNT)
                },
                'error_file_handler': {
                    'class': 'cloghandler.ConcurrentRotatingFileHandler' if self.multiprocess else 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'verbose_error',
                    'filename': LOG_PATH_ERROR,
                    'maxBytes': int(LOG_FILE_MAX_BYTES),
                    'backupCount': int(LOG_FILE_BACKUP_COUNT)
                }
            },
            'loggers': {
                'console_logger': {
                    'handlers': ['console'],
                    'level': self.log_level,
                    'propagate': False,
                },
                'file_logger': {
                    'handlers': ['info_file_handler', 'error_file_handler'],
                    'level': self.log_level,
                    'propagate': False,
                },
                'common_logger': {
                    'handlers': ['info_file_handler', 'error_file_handler'],
                    'level': self.log_level,
                    'propagate': True,
                },
            },
            'root': {
                'level': self.log_level,
                'handlers': ['console']
            }
        }

    @property
    def logger(self):
        if self.multiprocess:
            try:
                from cloghandler import ConcurrentRotatingFileHandler
            except ImportError as e:
                raise ImportError('未安装三方库ConcurrentLogHandler')

        # 创建日志目录
        try:
            os.makedirs(LOG_PATH)
        except OSError:
            pass
        dictConfig(self._logging_config)
        return logging.getLogger(self.log_type)
