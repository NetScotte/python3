# -*- coding=utf-8 -*-
from pathlib import Path

import click

from log import logger
from common import log_pid
from exceptions import ExceptionsParse
from cmd_context import pass_context


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, path, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    path = Path(path)
    try:
        indir = list(path.iterdir())
    except Exception as e:
        ExceptionsParse(e)
        exit(1)
    if indir:
        logger.debug('文件夹下内容:%s', indir)
        for i in indir:
            ctx.vlog(i)
        click.echo('本次程序文件有变更，需要进行打包任务。')
        exit(0)
    else:
        ctx.err('程序文件夹为空，不需要进行打包任务。')
        exit(1)


if __name__ == '__main__':
    main()
