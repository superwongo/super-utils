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
    def __init__(self, log_type=None, log_level=None, log_path=None, log_path_info=None, log_path_error=None,
                 log_file_max_bytes=None, log_file_backup_count=None, multiprocess=False):
        """
        :param log_type: 日志类型，console_logger、file_logger、common_logger
        :param log_level: 日志级别，DEBUG、INFO、ERROR、CRITICAL、EXCEPTION，默认INFO
        :param log_path: 日志目录
        :param log_path_info: 正常日志文件绝对路径
        :param log_path_error: 异常日志文件绝对路径
        :param log_file_max_bytes: 日志文件最大字节数，默认10M
        :param log_file_backup_count: 日志文件最大备份个数，默认10个
        :param multiprocess: 是否支持多进程，默认False
        """
        self.log_type = log_type or LOG_TYPE
        self.log_level = log_level or LOG_LEVEL
        self.multiprocess = multiprocess
        self.log_path = log_path or LOG_PATH
        self.log_path_info = log_path_info or LOG_PATH_INFO
        self.log_path_error = log_path_error or LOG_PATH_ERROR
        self.log_file_max_bytes = log_file_max_bytes or LOG_FILE_MAX_BYTES
        self.log_file_backup_count = log_file_backup_count or LOG_FILE_BACKUP_COUNT
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
                    'filename': self.log_path_info,
                    'maxBytes': int(self.log_file_max_bytes),
                    'backupCount': int(self.log_file_backup_count)
                },
                'error_file_handler': {
                    'class': 'cloghandler.ConcurrentRotatingFileHandler' if self.multiprocess else 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'verbose_error',
                    'filename': self.log_path_error,
                    'maxBytes': int(self.log_file_max_bytes),
                    'backupCount': int(self.log_file_backup_count)
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
            os.makedirs(self.log_path)
        except OSError:
            pass
        dictConfig(self._logging_config)
        return logging.getLogger(self.log_type)


if __name__ == '__main__':
    logger = LoggerGenerator().logger
    logger.debug('debug日志')
    logger.info('info日志')
    logger.error('error日志')
    logger.critical('critical日志')
    logger.exception('exception日志')
