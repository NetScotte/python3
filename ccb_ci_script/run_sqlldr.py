# -*- coding=utf-8 -*-
import pathlib
import subprocess

import click
import rarfile

from cmd_context import pass_context
from common import isolated_filesystem, b2s, log_pid
from exceptions import ExceptionsParse
from log import logger


def rar_check(rar_file):
    """检查rar文件内部目录机构是否符合规范
    将内部结构以字典的形式存储起来，形式如下：
    {
        '一级目录1': [子目录1, 子目录2,...],
        '一级目录2': [子目录1, 子目录2,...],
        ...
    }
    ctl，data，log必须在每个value中。

    :param rar_file: rar文件
    :type rar_file: rarfile.RarFile
    :return: 是否符合规范, 目录结构字典
    :rtype: bool, dict
    """

    directory_structure = {}  # 目录结构字典，用来最后判断结构是否正确
    for i in rar_file.infolist():
        if i.isdir():  # 提取所有目录性质的路径
            root = i.filename.split('/', 1)[0]  # 提取此路径的第一级目录作为根
            if len(i.filename.split('/', 1)) == 1:  # 判断此路径是否包含子目录
                if root in directory_structure:
                    # root在目录结构字典中已经有作为key存在
                    pass
                else:
                    # root在目录结构字典中作为key不存在，则以根为key，空list为value构建字典的一个元素
                    directory_structure.setdefault(root, [])
            else:  # 路径包含子目录
                if root in directory_structure:
                    # 检查root在目录结构字典中已经有作为key存在，
                    # 则将子目录部分加入到这个root为key的value中
                    directory_structure[root].append(
                        i.filename.split('/', 1)[1])
                else:
                    # 检查root在目录结构字典中没有作为key存在，
                    # 则将root为key，子目录部分为value构建字典元素
                    directory_structure.setdefault(
                        root, [i.filename.split('/', 1)[1]])
    # 校验目录结构是否符合要求
    for root, sub_dir in directory_structure.items():
        if ('ctl' in sub_dir) and ('data' in sub_dir) and ('log' in sub_dir):
            return True, directory_structure
        else:
            return False, directory_structure


@click.command()
@click.option('--username', help='数据库用户名')
@click.option('--password', help='数据库密码')
@click.option('--tnsname', help='tnsname')
@click.option('--dir_path', type=click.Path(), help='sqllrd压缩包所属路径')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='调试模式')
@pass_context
def main(ctx, username, password, tnsname, dir_path, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    # 判断文件verbose夹是否存在
    try:
        if not pathlib.Path(dir_path).exists():
            click.echo(f'{pathlib.Path(dir_path).resolve()}不存在。')
            exit(0)
    except Exception as e:
        ExceptionsParse(e)
        exit(1)
    # 逐个解压rar文件
    for rar_file in pathlib.Path(dir_path).glob('*.[Rr][Aa][Rr]'):
        with isolated_filesystem():
            with rarfile.RarFile(rar_file.as_posix()) as rf:
                # rar内部结构检查
                rar_check_result, directory_structure = rar_check(rf)
                if rar_check_result:
                    logger.info(f'{rar_file}内部结构:{directory_structure}')
                    click.echo(f'>>>>>>>>>>正在解压{rar_file}')
                    rf.extractall()  # 解压缩到当前目录
                else:
                    logger.info(f'{rar_file}内部结构:{directory_structure}')
                    ctx.err(f'{rar_file}文件内部结构不符合规范。')
                    exit(1)
                # 递归解压开的每个文件夹
                for d in pathlib.Path.cwd().iterdir():
                    # 逐个执行ctl文件
                    for ctl_file in ((d / 'ctl').glob('*.ctl')):
                        click.echo(f'>>>>>>>>>>执行{rar_file/ctl_file}开始')
                        logfile = ctl_file.parent.parent / 'log' / f'{ctl_file.name}.log'
                        command = f'sqlldr {username}/{password}@{tnsname} control="{ctl_file.resolve()}" log="{logfile.resolve()}"'
                        logger.info(command)
                        p = subprocess.Popen(
                            command,
                            cwd=pathlib.Path.cwd() / d,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        stdout, stderr = p.communicate()
                        logger.info(b2s(stdout))
                        if p.returncode == 0:
                            click.echo(f'>>>>>>>>>>执行{rar_file/ctl_file}完毕')
                        else:
                            ctx.err(logfile.read_text())
                            ctx.err(b2s(stderr))
                            ctx.err(f'执行{rar_file/ctl_file}失败')
                            exit(1)


if __name__ == '__main__':
    main()
