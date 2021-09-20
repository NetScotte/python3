# -*- coding=utf-8 -*-
import os
from collections import OrderedDict

import click
# import prettytable

from cmd_context import pass_context
from common import log_pid
from log import logger


def getdir(path):
    """遍历path目录下所有文件，返回一个生成器

    :param path: 绝对路径
    :type path: str
    :return: 文件(绝对路径)
    :rtype: generator
    """
    for root, dirs, files in os.walk(path):
        for f in files:
            yield os.path.join(root, f)


@click.command()
@click.option('--directory', type=click.Path(exists=True))
# @click.option(
#     '-e',
#     '--ext_name',
#     help=u'需要统计的文件扩展名',
#     default=('java',),
#     type=tuple,
#     metavar='<string>')
@click.option("--taskid")
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option("--debug", is_flag=True, help='开启debug')
@pass_context
def main(ctx, directory, taskid, verbose, debug):
    """从文件夹中统计各个类型文件数量"""
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    ext_name = ('java',)
    logger.info(f"传入参数> directory:{directory}, ext_name:{ext_name}")
    ext_name = sorted(list(ext_name))
    logger.info(f"ext_name排序结果:{ext_name}")
    result = {}
    directory = [directory]
    for _dir in directory:
        # 构建文件类型统计字典 {'java':[], ... ,'other':[]}，根据扩展名排序
        data = OrderedDict(
            sorted({ext: []
                    for ext in ext_name}.items(), key=lambda x: x[0]))
        data['other'] = []
        path = os.path.abspath(_dir)
        for i in getdir(path):
            name, ext = os.path.splitext(i)
            if ext[1:] in data:  # 去掉扩展名前面的“.”后判断是否在统计范围内
                data[ext[1:]].append(i)
            else:
                data['other'].append(i)
        # 统计好一个文件夹后存入result中
        result.setdefault(os.path.abspath(_dir), data)
    click.echo(f'''Java file count: {len(data['java'])}. Other file count: {len(data['other'])}.''')
    # tb = prettytable.PrettyTable()
    # tb.field_names = ['目录'] + [f'{i}文件数量' for i in ext_name] + ['other文件数量']
    # ext_sum = [0] * (len(ext_name) + 1)
    # for _dir, data in result.items():
    #     every_ext_count = [len(data[e]) for e, file_list in data.items()]
    #     ctx.vlog(f"文件夹:{_dir}。统计数据:{dict(zip(ext_name, every_ext_count))}")
    #     tb.add_row([_dir] + every_ext_count)
    #     # 各个类型文件数量求和
    #     ext_sum = list(
    #         map(lambda x: x[0] + x[1], zip(ext_sum, every_ext_count)))
    # tb.add_row(['总计'] + ext_sum)
    # tb.align[u"目录"] = "l"
    # click.echo(" ")
    # click.echo(tb)


if __name__ == "__main__":
    main()
