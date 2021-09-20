# -*- coding=utf-8 -*-

import click
import sys

@click.command()
@click.option('--taskid')
def main(taskid):
    print('print输出')
    click.echo('echo输出')
    sys.exit(6)

if __name__ == '__main__':
    main()
