# -*- coding=utf-8 -*-
import pathlib
import shutil
import svn.remote

import click

from cmd_context import pass_context
from common import b2s, onerror, log_pid
from log import logger
from exceptions import ExceptionsParse
"""svn export脚本
用法:
python svn_export.py --url URL --path PATH [--method clean|override]\
        [--username] [--password]

注意:
导出路径处理模式:
1. 没有method方式。路径不存在则创建，存在则报错
2. method参数为clean。路径不存在则创建，存在则重建
3. method参数为override。路径不存在则创建，存在则覆盖
"""


class MyRemoteClient(svn.remote.RemoteClient):
    def __init__(self, url, *args, **kwargs):
        self.__url = url
        super(MyRemoteClient, self).__init__(url, *args, **kwargs)

    def export(self, to_path, revision=None, force=False, return_binary=False):
        cmd = []

        if revision is not None:
            cmd += ['-r', str(revision)]

        cmd += [self.__url, to_path]
        cmd.append('--force') if force else None

        return self.run_command('export', cmd, return_binary=return_binary)


@click.command()
@click.option('--url', help='svn url')
@click.option('--path', help='导出路径')
@click.option(
    '--method',
    type=click.Choice(['clean', 'override']),
    help='导出方式，1.清空目录。2.覆盖目录')
@click.option('--username', help='svn用户名')
@click.option('--password', help='svn密码')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, url, path, method, username, password, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    path = pathlib.Path(path)
    force = False
    if path.exists():
        ctx.vlog(f'<{path.resolve()}>已经存在')
        if method == 'clean':
            ctx.vlog(f'清空<{path.resolve()}>')
            shutil.rmtree(path, onerror=onerror)
            path.mkdir(parents=True)
            ctx.vlog(f'清空完毕')
        elif method == 'override':
            ctx.vlog('覆盖模式导出')
            force = True
        else:
            pass
    else:
        path.mkdir(parents=True)
    remote_client = MyRemoteClient(
        url, username=username, password=password)
    path_string = str(path)
    try:
        result = remote_client.export(to_path=path_string, force=True, return_binary=True)
    except Exception as e:
        ExceptionsParse(e)
        ctx.err('导出失败T_T')
        exit(1)
    else:
        ctx.vlog(b2s(result))
        click.echo('导出成功^_^')


if __name__ == '__main__':
    main()
