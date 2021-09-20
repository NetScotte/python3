# -*- coding: utf-8 -*-
"""
功能：单元测试的练习或功能测试
设计：
备注：
时间：
"""
import unittest


def func1(a):
    return a + 1


class MyFuncTest(unittest.TestCase):
    def setUp(self):
        print("start to test")

    def tearDown(self):
        print("end test")

    def test_func1(self):
        a_cases = [-1, 0, 23, 0.1, "1", "h", ['1', 2], {"name": "error"}]
        for a in a_cases:
            with self.subTest(a=a):
                func1(a)

    def test_func1_typeerror(self):
        a_cases = ["h", [1, "2"], {"name": "error"}]
        for a in a_cases:
            with self.subTest(a=a):
                self.assertRaises(TypeError, func1, a)


if __name__ == "__main__":
    unittest.main(module="test_func1", verbosity=2)
