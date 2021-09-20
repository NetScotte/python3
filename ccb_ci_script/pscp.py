# -*- coding=utf-8 -*-
import click
import os
import pathlib
import glob
import paramiko
import socket

from cmd_context import pass_context
from common import log_pid
from log import logger
from exceptions import ExceptionsParse


def put_dir(ctx, sftp, source, target):
    '''上传文件夹至目标目录'''
    ctx.vlog(f'远程创建目录{pathlib.Path(target).joinpath(source.name).as_posix()}')
    try:
        sftp.stat(pathlib.Path(target).joinpath(source.name).as_posix())
    except FileNotFoundError:
        sftp.mkdir(pathlib.Path(target).joinpath(source.name).as_posix())
        logger.info(
            f'远程目录<{pathlib.Path(target).joinpath(source.name).as_posix()}>创建完毕'
        )
    for item in os.listdir(source):
        if source.joinpath(item).is_file():
            logger.info(
                f'''正在传输文件<{source.joinpath(item)}>到<{pathlib.Path(target).joinpath(source.name, item).as_posix()}>'''
            )
            sftp.put(
                source.joinpath(item),
                pathlib.Path(target).joinpath(source.name, item).as_posix())
        elif source.joinpath(item).is_dir():
            logger.info(
                f'''正在传输<{source.joinpath(item)}>到<{os.path.join(target, source.name)}>'''
            )
            put_dir(ctx, sftp, source.joinpath(item),
                    f'{os.path.join(target, source.name)}')
        else:
            ctx.err(f'<{source.joinpath(item)}>不是文件也不是文件夹。')


@click.command()
@click.argument('source', required=True)
@click.argument('hostname')
@click.option('--port', default=22, help='端口号')
@click.option('--username', '-u', default=None, help='用户名')
@click.option('--password', '-p', default=None, help='密码')
@click.argument('path')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='调试模式')
@pass_context
def main(ctx, source, hostname, port, username, password, path, taskid,
         verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    try:
        t = paramiko.Transport((hostname, port))
    except socket.gaierror as e:
        logger.error(e)
        ctx.err('无法解析远程主机地址')
        exit(1)
    except paramiko.ssh_exception.SSHException as e:
        logger.error(e)
        ctx.err('无法链接远程主机。')
        exit(1)
    try:
        t.connect(username=username, password=password)
        logger.info('远程主机链接成功!')
        sftp = paramiko.SFTPClient.from_transport(t)
    except paramiko.ssh_exception.AuthenticationException as e:
        ctx.err('远程主机认证失败。')
        t.close()
        exit(1)
    except Exception as e:
        ExceptionsParse(e)
        t.close()
        exit(1)

    # 通配符获取源文件
    source_list = glob.glob(source, recursive=True)
    logger.debug('传输文件通配符结果：%s', source_list)
    if not source_list:
        ctx.err('源文件不存在。')
        t.close()
        exit(0)

    # 校验远程目录是否存在
    try:
        sftp.stat(path)
    except FileNotFoundError:
        ctx.err('远程主机目录不存在。')
        t.close()
        exit(1)

    for i in source_list:
        _source = pathlib.Path(i)
        if _source.is_dir():
            logger.info(f'''正在传输<{_source}>到<{path}>''')
            put_dir(ctx, sftp, _source, path)
        else:
            logger.info(f'''正在传输文件<{_source}>到<{path}>''')
            sftp.put(_source.as_posix(),
                     pathlib.Path(path).joinpath(_source.name).as_posix())
    click.echo(f'传输{source_list}到{hostname}:{path}成功。')
    t.close()


if __name__ == '__main__':
    main()
