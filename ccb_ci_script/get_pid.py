# -*- coding=utf-8 -*-
import subprocess
import os

import click

from common import log_pid


@click.command()
@click.option('--taskid')
def main(taskid):
    log_pid(taskid)
    print('Main process begin...')
    p = subprocess.Popen('sleep 30', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'This is sub process :{os.getpgid(p.pid)}')
    p.communicate()


if __name__ == '__main__':
    main()
