# -*- coding: utf-8 -*-
"""
功能：sample getopt and getpass
设计：
参数：
作者: netliu
时间：
"""
import getopt
import getpass
import sys


def get_cmdopts():
    opts, args = getopt.getopt(sys.argv[1:], 'nvmda:u:p:f:ht')
    for opt, arg in opts:
        print(opt, arg)

    password = getpass.getpass(prompt="Password: ")
    print(password)
