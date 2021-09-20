# -*- coding=utf-8 -*-
import click

from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import log_pid
"""
命令行工具模板(正式编辑请先修改！)
"""


@click.command()
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, taskid, verbose, debug):
    # 根据debug参数开启debug功能
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose

    # 在此开始脚本代码
    # 1.verbose输出,通过ctx.vlog()
    # 2.ExceptionsParse来解析try所捕获到的Excepion
    # 3.使用logger作为日志记录器,使用发放与内置logging库一致
    # 4.异常退出返回码用exit(1)


if __name__ == '__main__':
    main()
