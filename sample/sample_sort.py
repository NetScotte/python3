# -*- coding: utf-8 -*-
"""
功能：
    排序对象是列表
    默认从小到大排列
    sort()  修改原列表
    sorted()    产生新列表
    参数key用于指定对象的某个属性用来进行比较
设计：
参数：
作者: netliu
时间：
"""
# 对数字排序
sample_list_digit = [1, 3, 0, -1, 4, 1, 2]
print(sorted(sample_list_digit))

# 对字符排序
sample_list_char = ["a", "c", "A", "d"]     # 大写字母比小写字母的序列小
print(sorted(sample_list_char, reverse=True))

# 对字典排序
sample_dict = [{"name": "a", "age": 11}, {"name": "b", "age": 13}, {"name": "b", "age": 10}]
print(sorted(sample_dict, key=lambda info: info["age"]))

# 指定函数来比较
def getKey(stu):
    return stu["age"] % 12

sample_dict = [{"name": "a", "age": 4}, {"name": "b", "age": 24}, {"name": "b", "age": 56}]
print(sorted(sample_dict, key=getKey))
