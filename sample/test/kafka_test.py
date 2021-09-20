# -*- coding: utf-8 -*-
"""
功能：
设计：
备注：
时间：
"""
import unittest
from sample.sample_kafka import KafkaDaemon


class MyUnittest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj_ins = KafkaDaemon(["192.168.1.105:9092"])

    def test_kafka_send(self):
        messages = ['', 123, None, "this is normal", "123aa", {"dict": "test"}]
        for message in messages:
            self.obj_ins.send(message)

    def test_kafka_get(self):
        self.assertTrue(self.obj_ins.get())

    def test_info(self):
        self.obj_ins.info()

    @classmethod
    def tearDownClass(cls):
        cls.obj_ins.close()
