# -*- coding=utf-8 -*-
import click
from pathlib import Path
import shutil

from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import log_pid, onerror
import _zipfile as zipfile


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, source, target, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    logger.debug(f"传入参数:{source}, {target}, {taskid}")
    log_pid(taskid)

    source_path, target_path = Path(source), Path(target)
    if source_path.resolve() == target_path.resolve():
        logger.warn('源:<%s>,目的:<%s>一致', source_path, target_path)
        ctx.err(f'源与目标路径不能为同一路径')
        exit(1)
    try:
        if not target_path.exists():
            logger.info('%s不存在，正在创建', target_path)
            target_path.mkdir(parents=True)
            logger.info('%s创建完毕', target_path)
        else:
            logger.warn('%s已存在，正在删除重建', target_path)
            shutil.rmtree(target_path, onerror=onerror)
            logger.info('%s已经删除', target_path)
            target_path.mkdir(parents=True)
            logger.info('%s已经创建完毕', target_path)
    except Exception as e:
        ExceptionsParse(e)
        exit(1)

    zip_file_list = [
        i for i in source_path.iterdir() if i.suffix.upper() == '.ZIP'
    ]
    logger.debug('%s路径下的压缩包为:%s', source_path, zip_file_list)
    if len(zip_file_list) == 0:
        ctx.err(f'{source_path}路径下不存在压缩包,请核对。')
        exit(1)
    elif len(zip_file_list) > 1:
        ctx.err(f'{source_path}路径下存在多个压缩包,请核对。')
        exit(1)

    logger.info('开始解压缩%s...', zip_file_list[0])
    zip_file = zipfile.ZipFile(zip_file_list[0].resolve())
    logger.debug('解压缩文件绝对路径:%s', zip_file)
    logger.debug('解压缩目标目录绝对路径:%s', target_path.resolve())
    zip_file.extractall(path=target_path.resolve())
    click.echo(f'解压缩 [{zip_file_list[0].name}] 完毕!')


if __name__ == "__main__":
    main()
