# -*- coding=utf-8 -*-
import pathlib
import subprocess
import os

import click

from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import log_pid, b2s
"""
命令行工具模板
"""


@click.command()
@click.argument('build_xml', type=click.Path(exists=True))
@click.option('--src', type=click.Path(exists=True))
@click.option('--dst', default='dist')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, build_xml, src, dst, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)

    if src:
        for root, dirs, files in os.walk(src):  # 判断是否有编译文件
            if files:
                break
        else:
            click.echo('源文件夹下没有需要编译的文件，无需执行编译任务！')
            exit(0)
    build_xml_ = pathlib.Path(build_xml)
    complie_command = f'ant -f {build_xml_} {dst}'
    p = subprocess.Popen(
        complie_command,
        cwd=build_xml_.parent,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        click.echo(b2s(stdout))
    else:
        ctx.err(b2s(stdout))
        ctx.err(b2s(stderr))
        exit(1)


if __name__ == '__main__':
    main()
