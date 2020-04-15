#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: wang_chao03
@project: super-utils
@file: daemon.py
@time: 2020/04/15
"""

from __future__ import print_function
import sys
import os
import time
import atexit
import signal

py_version = sys.version_info.major


class Daemon(object):
    """A generic daemon class.
        Usage: subclass the daemon class and override the run() method.
    """
    def __init__(self, pid_file, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.pid_file = pid_file
        self.stdin = stdin if py_version < 3 else os.devnull
        self.stdout = stdout if py_version < 3 else os.devnull
        self.stderr = stderr if py_version < 3 else os.devnull

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pid_file
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pid_file, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pid_file)

    def start(self):
        """Start the daemon."""

        # Check for a pid_file to see if the daemon already runs
        try:
            with open(self.pid_file, 'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pid_file {0} already exist. " + \
                      "Daemon already running?\n"
            sys.stderr.write(message.format(self.pid_file))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()
        return pid

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pid_file
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pid_file {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pid_file))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            else:
                print(str(err.args))
                sys.exit(1)
        return pid

    def restart(self):
        """Restart the daemon."""
        self.stop()
        return self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""


if __name__ == '__main__':
    def get_args():
        """脚本执行参数获取"""
        import argparse
        parser = argparse.ArgumentParser(description='Daemon进程发起脚本')
        parser.add_argument('option', choices=['start', 'stop', 'restart'], help='操作方式')
        return parser.parse_args()

    def server():
        while True:
            pass

    class ServerDaemon(Daemon):
        def __init__(self, pid_file_path):
            super(ServerDaemon, self).__init__(pid_file_path)

        def run(self):
            server()

    root_path = os.path.dirname(os.path.abspath(__file__))
    sd = ServerDaemon(os.path.join(root_path, 'server_daemon.pid'))
    args = get_args()
    if args.option == 'start':
        pid = sd.start()
        print('>>>>>服务已启动完成，进程号：{}'.format(pid))
    elif args.option == 'stop':
        sd.stop()
        print('>>>>>服务已停止')
    elif args.option == 'restart':
        pid = sd.restart()
        print('>>>>>服务已重启完成，新进程号：{}'.format(pid))
