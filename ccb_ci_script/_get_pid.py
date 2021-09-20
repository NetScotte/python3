# -*- coding=utf-8 -*-
import subprocess
import os

import click

from common import log_pid
from log import logger
"""此文件为pid功能测试文件"""


@click.command()
@click.option('--taskid')
@click.option('--debug', is_flag=True)
def main(taskid, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    logger.info('Main process begin...')
    p = subprocess.Popen('sleep 5', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.debug_off()
    logger.error(f'This is sub process :{os.getpgid(p.pid)}')
    p.communicate()


if __name__ == '__main__':
    main()
