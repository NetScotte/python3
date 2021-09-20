# -*- coding=utf-8 -*-
import pathlib
import subprocess
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
@click.option('--target', help='checkstyle报告输出路径')
@click.option('--report', help='html报告url')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, build_xml, target, report, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)

    build_xml_ = pathlib.Path(build_xml)
    target_ = pathlib.Path(target)
    complie_command = f'ant -f {build_xml_} -DcheckstyleFile={target_}'
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
        click.echo(f'静态代码扫描报告请查阅 <a href= "{report}" target="_blank">查看报告</a>')
    else:
        ctx.err(b2s(stderr))
        exit(1)


if __name__ == '__main__':
    main()
