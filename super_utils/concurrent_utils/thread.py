#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: thread.py
@time: 2020/04/13
"""

import multiprocessing
from multiprocessing.pool import ThreadPool


def thread_apply_async(task_list):
    """
    线程池异步调用
    :param task_list: 任务列表
    :return: 进程池异步执行结果列表
    """
    if not task_list:
        return []
    num_cpu = multiprocessing.cpu_count() * 2 + 1
    pool = ThreadPool(processes=min(len(task_list), num_cpu))
    threads = []
    for task, args in task_list:
        t = pool.apply_async(task, args=args)
        threads.append(t)
    pool.close()
    pool.join()
    query_result = []
    for t in threads:
        query_result.append(t.get())
    return query_result


if __name__ == '__main__':
    def test(value1, value2=None):
        pass

    results = thread_apply_async([(test, ('1', '2')),])
