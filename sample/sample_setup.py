# -*- coding: utf-8 -*-
"""
功能：setup示例
设计：
参数：
作者: netliu
时间：
"""
from setuptools import setup

setup(
    name='svcstats.py',
    version='1.0.3.1',
    py_modules=['svcstats'],
    install_requires=['pywbem'],
    url='https://gitlab.com/mezantrop/svcstats.py',
    license='',
    author='Mikhail Zakharov',
    author_email='zmey20000@yahoo.com',
    description='Report IBM SVC/Storwize storage system performance statistics for nodes, vdisks, mdisks or drives in CLI'
)
