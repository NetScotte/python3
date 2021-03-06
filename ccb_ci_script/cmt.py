# -*- coding=utf-8 -*-
import pathlib
import shutil
import zipfile
import os
import datetime

import click

from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import log_pid, onerror


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for dir in dirs:
                filelist.append(os.path.join(root, dir))
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(str(dirname)):]
        zf.write(tar, arcname)
    zf.close()


@click.command()
@click.argument('workspace')
@click.argument('package_name')
@click.option(
    '--timestamp',
    default=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
    help='打包文件时间戳')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, workspace, package_name, timestamp, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)

    base_dir = pathlib.Path(workspace)
    logger.debug('基础工作目录:%s', base_dir)
    # 版本包文件夹
    package = base_dir / package_name
    logger.debug('版本包目录:%s', package)
    # copy src/sql到打包文件夹
    if package.exists():
        shutil.rmtree(package, onerror=onerror)
    sql = base_dir / 'src' / 'sql'
    sql_ = package / 'sql'
    if sql.exists():
        shutil.copytree(sql, sql_)
        logger.debug('拷贝sql到版本包成功')
    # 将“程序”拷贝到package目录
    dist = base_dir / 'dist'
    shutil.copytree(dist, package / 'package')
    logger.debug('拷贝dist到%s中', package_name)

    # 判断package下是否为空文件夹
    for root, dirs, files in os.walk(package, topdown=False):
        if not files:
            try:
                pathlib.Path(root).rmdir()
                logger.debug('%s为空文件夹，即将删除', root)
            except OSError:
                logger.debug('%s里有文件夹存有文件，不删除。', root)
    if not package.exists():
        ctx.err('打包文件夹里没有文件，请核对')
        exit(1)

    zf = base_dir / (package_name + timestamp + '.zip')
    logger.debug('开始打包')
    zip_dir(package, zf)
    click.echo(f'{package_name}打包完成')


if __name__ == '__main__':
    main()
