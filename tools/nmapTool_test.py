# -*- coding: utf-8 -*-
"""
功能：
设计：
参数：
作者: netliu
时间：
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.nmapTool import *


class nmapTool_test(unittest.TestCase):
    def test_get_alive_hosts(self):
        hosts = "172.16.18.21/24"
        results = get_alive_hosts(hosts=hosts)
        print(results)

    def test_get_basic_info(self):
        hosts = ["172.16.18.1", "172.16.18.3", "172.16.18.11", "172.16.18.13", "172.16.18.17", "172.16.18.18"]
        results = get_basic_info(hosts)
        print(results)
