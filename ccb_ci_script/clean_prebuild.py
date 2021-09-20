# -*- coding=utf-8 -*-
import shutil
import pathlib

import click

from cmd_context import pass_context
from common import onerror
from exceptions import ExceptionsParse
from common import log_pid
from log import logger

regx_list = [r"^C:"]
exact_list = [
    r"^D:[/\\]{0,1}",
    r"^D:[/\\]{1}deploy[/\\]{0,1}",
    r"^D:[/\\]{1}Python36[/\\]{0,1}",
    r"^D:[/\\]{1}maven_repo[/\\]{0,1}",
    r"^D:[/\\]{1}shepherd_kala[/\\]{0,1}",
    r"^D:[/\\]{1}tool[/\\]{0,1}",
]


@click.command()
@click.option("--target", type=click.Path(), help="清理目标路径")
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
@click.pass_context
def main(_ctx, ctx, target, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    # 参数校验
    ctx.check_param(_ctx.params, regx_list, exact_list)
    ctx.verbose = verbose

    clean_target = pathlib.Path(target)
    try:
        if not clean_target.exists():
            click.echo(f"{clean_target}不存在，无需清理。")
            exit(0)
        shutil.rmtree(target, onerror=onerror)
    except Exception as e:
        ExceptionsParse(e)
        exit(1)
    else:
        click.echo("执行删除成功。")
        exit(0)


if __name__ == "__main__":
    main()
