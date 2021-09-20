# -*- coding=utf-8 -*-
import logging
import os
import subprocess

import click

from log import logger
from common import b2s, log_pid
from cmd_context import pass_context
from exceptions import ExceptionsParse


class CompressUnsupport(BaseException):
    pass


class RunCommandError(BaseException):
    pass


class MissFile(BaseException):
    pass


def test_compressed_file(path, compressed_file):
    """查看压缩文件中class文件和其他类型文件的数量

    Arguments:
        path {string} -- 压缩文件绝对路径
        compressed_file {string} -- 压缩文件文件名

    Raises:
        MissFile -- 打包文件不存在
        CompressUnsupport -- 不支持的压缩格式
        RunCommandError -- 运行测试命令报错

    Returns:
        tuple -- (class文件数量, 其他类型文件数量)
    """
    filename, extension = os.path.splitext(compressed_file)
    args = {
        "cwd": path,
        "shell": True,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE
    }
    # 判断压缩格式
    if extension == '.zip':
        command = "unzip -l %s" % compressed_file
        if not os.path.exists(os.path.join(path, compressed_file)):
            raise MissFile('打包文件{}不存在'.format(
                os.path.join(path, compressed_file)))
    elif extension == '.tar':
        raise CompressUnsupport("不支持tar压缩格式")
    elif extension == '.rar':
        raise CompressUnsupport("不支持rar压缩格式")
    # 执行测试命令
    p = subprocess.Popen(command, **args)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        pass
    else:
        raise RunCommandError(stderr.strip())

    # 解析输出结果
    _class_file_count = 0
    _other_file_count = 0
    if extension == '.zip':
        for line in b2s(stdout).splitlines()[3:-2]:
            # 去掉行首空格，然后根据三个空格分割一次，来取到文件名
            name = line.strip().split("   ")[1]
            if name.endswith("/"):
                continue
            if os.path.splitext(name)[1] == '.class':
                _class_file_count += 1
            else:
                _other_file_count += 1
    elif extension == '.tar':
        pass
    elif extension == '.rar':
        pass

    return _class_file_count, _other_file_count


@click.command()
@click.option("--username", help="svn账号")
@click.option("--password", help="svn密码")
@click.option("--branch", help="分支url")
@click.option("--revision", type=int, help="分支上次记录版本号")
@click.option("--path", help="打包文件路径")
@click.option("--package", help="打包文件文件名")
@click.option("--java_count", type=int, help="上次记录java文件数量")
@click.option("--other_count", type=int, help="上次记录其他文件数量")
@click.option("--taskid")
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option("--debug", is_flag=True)
@pass_context
def cli(ctx, username, password, branch, revision, path, package, java_count,
        other_count, taskid, verbose, debug):
    # 获取分支最新版本号
    log_pid(taskid)
    ctx.verbose = verbose
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug(
        '\n'
        '===传入参数==========================================================================\n'
        'username(svn账号):{username}   password(svn密码):{password}\n'
        'branch(分支):{branch}   revision(上次记录分支版本号):{revision}\n'
        'path(打包文件路径):{path}   package(打包文件文件名):{package}\n'
        'java_count(上次记录java文件数量):{java_count}   other_count(上次记录其他文件数量):{other_count}\n'
        '======================================================================================'.
        format(
            username=username,
            password=password,
            branch=branch,
            revision=revision,
            path=path,
            package=package,
            java_count=java_count,
            other_count=other_count))
    logger.debug('开始获取分支最新版本号...')
    command1 = "svn info --username %s --password %s %s" % (username, password,
                                                            branch)
    p1 = subprocess.Popen(
        command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p1.communicate()
    # FIXME:命令执行报错时候需要处理错误
    for i in b2s(stdout).splitlines():
        logger.debug(i)
        if "Last Changed Rev" in i:
            last_revision = int(i.split(":")[-1])
    logger.debug('分支最新版本号:{}'.format(last_revision))

    # 获取打包文件中的文件数量
    logger.debug('开始统计打包文件内各文件数量...')
    try:
        _class_file_count, _other_file_count = test_compressed_file(
            path, package)
        logger.debug('class文件数量:{}'.format(_class_file_count))
        logger.debug('其他文件数量:{}'.format(_other_file_count))
    except CompressUnsupport as e:
        ctx.err('不知道的压缩格式')
        exit(1)
    except MissFile as e:
        ctx.err('压缩文件不存在')
        exit(1)
    except RunCommandError as e:
        ExceptionsParse(e)
        ctx.err('运行失败，请联系管理员!')
        exit(1)

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
    cli()
