# -*- coding=utf-8 -*-
import subprocess
import shlex

import click
from cmd_context import pass_context
from common import b2s


@click.command()
@click.option('--command', help='命令')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, command, debug):
    ctx.debug = debug
    seq_command = shlex.split(command)
    ctx.vlog(command)
    ctx.vlog(seq_command)
    p = subprocess.Popen(
        seq_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        click.echo(b2s(stdout))
        exit(0)
    else:
        ctx.err(b2s(stderr))
        exit(1)


if __name__ == '__main__':
    main()
