# -*- coding: utf-8 -*-
"""
功能：args功能测试
设计：
    设计一个参数解析示例代码，覆盖常见的选项
备注：
时间：2018-08-27
"""
import argparse


def sample_argument():
    parser = argparse.ArgumentParser(description="typically argument daemon")
    parser.add_argument("name", help="user name")
    parser.add_argument("age", type=int, help="user age")
    parser.add_argument("-g", "--gender", help="user gender", choices=['M', 'F'])
    parser.add_argument("-b", "--brother", help="user brother", action="append")
    parser.add_argument("-i", "--info", type=argparse.FileType("r"), help="user info file")
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()
    print(args)


def comment_argument():
    parser = argparse.ArgumentParser(description="simple test")
    # prog, 程序名
    # description
    parser.add_argument("-picture", help="picture path", required=True)
    # name, 不带前导线表示位置参数，否则表示可选参数, 简称可以使用add_argument("-f", "--foo")
    # action：
    #   store, 保存信息，默认
    #   store_const, 根据const参数保存
    #   append, 场景-foo 1 -foo 2，可以得到[1, 2]
    #   count, 场景-v, -vv, 根据个数区分显示级别
    #   version， 场景，version="2.0", 显示版本信息
    # nargs, 值个数, 整数限定个数，?表示0到1个，*表示任意个，+至少一个
    # default, 默认值，可以为sys.stdin, sys.stdout表示执行时输入或执行时输出
    # type，限定参数类型，检查参数类型，如int, float, open, argparse.FileType("r")
    # choice, 枚举
    # help，参数描述
    # required，让可选参数称为必选
    # metar, 示例值
    # dest, 将值传递给该参数

    # 显示此parser的帮助信息
    parser.print_help()
    args, unknown = parser.parse_known_args()


if __name__ == "__main__":
    sample_argument()
