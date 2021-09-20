# -*- coding=utf-8 -*-
import os
from collections import OrderedDict

import click
import prettytable
import svn.remote

from cmd_context import pass_context
from exceptions import ExceptionsParse
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
@click.argument(
    'directory', type=click.Path(exists=True), nargs=-1, required=True)
@click.option(
    '-e',
    '--ext_name',
    help='需要统计的文件扩展名',
    multiple=True,
    metavar='<string>',
    required=True)
@click.option("--username", help="svn账号")
@click.option("--password", help="svn密码")
@click.option("--branch", help="分支url", required=True)
@click.option("--revision", type=int, help="分支上次记录版本号", required=True)
@click.option("--java_count", type=int, help="上次记录java文件数量", required=True)
@click.option("--other_count", type=int, help="上次记录其他文件数量", required=True)
@click.option("--taskid")
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option("--debug", is_flag=True, help='开启debug')
@pass_context
def main(ctx, directory, ext_name, username, password, branch, revision,
         java_count, other_count, taskid, verbose, debug):
    """从文件夹中统计各个类型文件数量"""
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    logger.info(f"传入参数> directory:{directory}, ext_name:{ext_name}")
    ext_name = sorted(list(ext_name))
    logger.info(f"ext_name排序结果:{ext_name}")
    result = {}
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

    # 定义输出表格
    tb = prettytable.PrettyTable()
    # 定制表头
    tb.field_names = ['目录'] + [f'{i}文件数量' for i in ext_name] + ['other文件数量']
    #  总和列表，加一是为了其他文件数量
    ext_sum = [0] * (len(ext_name) + 1)
    for _dir, data in result.items():
        every_ext_count = [len(data[e]) for e, file_list in data.items()]
        logger.info(f"文件夹:{_dir}。统计数据:{dict(zip(ext_name, every_ext_count))}")
        tb.add_row([_dir] + every_ext_count)
        # 各个类型文件数量求和
        ext_sum = list(
            map(lambda x: x[0] + x[1], zip(ext_sum, every_ext_count)))
    tb.add_row(['总计'] + ext_sum)
    tb.align['目录'] = "l"
    click.echo("")
    click.echo(tb)
    total_result = dict(zip(ext_name + ['other'], ext_sum))
    logger.info(f'''文件统计总和:{total_result}''')

    # 获取最新版本分支
    remote_client = svn.remote.RemoteClient(
        branch, username=username, password=password)
    try:
        last_revision = remote_client.info().get('commit#revision')
    except Exception as e:
        ExceptionsParse(e)
        exit(1)

    if 'class' not in total_result:
        ctx.err('class文件没有统计，无法进行版本检查。')
        exit(1)
    else:
        _class_file_count = total_result['class']
        _other_file_count = total_result['other']
    # 版本比较
    if (_class_file_count >= java_count) and (
            _other_file_count == other_count) and (revision == last_revision):
        click.echo("merge后分支版本号:%s。最新分支号:%s。" % (revision, last_revision))
        click.echo("Java文件数量:%s。Class文件数量:%s。" % (java_count,
                                                  _class_file_count))
        click.echo("merge后非Java文件数量:%s。打包后非Class文件数量:%s。" %
                   (other_count, _other_file_count))
        click.echo("版本检测通过")
        exit(0)
    else:
        if _class_file_count < java_count:
            click.echo("Class文件数量:%s。Java文件数量:%s。" % (_class_file_count,
                                                      java_count))
            click.echo("Class文件数量应该大于等于Java文件数量")
        if _other_file_count != other_count:
            click.echo("merge后非java文件数量:%s，打包后非class文件数量:%s。" %
                       (other_count, _other_file_count))
            click.echo("打包编译后非java文件数量有变化。")
        if revision != last_revision:
            click.echo("分支最新版本号:%s。打包编译的时候为:%s。" % (last_revision, revision))
        click.echo("版本检查失败!")
        exit(1)


if __name__ == "__main__":
    main()
