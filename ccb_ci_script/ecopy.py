# -*- coding=utf-8 -*-
import click
import pathlib
import os
import shutil

from cmd_context import pass_context
from common import log_pid
from log import logger
from exceptions import ExceptionsParse
"""
将SOURCE目录下的文件拷贝到TARGET文件夹下
适用方法：
python ecopy.py --source SOURCE --target TARGET [--exclude dir1] [--exclude dir2]
注意事项：
当目标路径不存在时，自动创建。
"""


@click.command()
@click.option('--source', type=click.Path(), help='源路径(目录)')
@click.option('--target', type=click.Path(), help='目标路径(目录)')
@click.option('--exclude', 'special', flag_value='exclude')
@click.option('--include', 'special', flag_value='include')
@click.option('--especial_file', '-e', multiple=True)
@click.option('--create_target', is_flag=True, help='强制创建目标目录')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='调试模式')
@pass_context
def main(ctx, source, target, special, especial_file, create_target, taskid,
         verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    _source = pathlib.Path(source)  # 将源目转换成Path类
    _target = pathlib.Path(target)

    if not _target.exists():
        if create_target:
            _target.mkdir(parents=True)
        else:  # 目标不存在且没有强制创建参数
            ctx.err('目标路径文件夹不存在')
            exit(1)
    if not _source.exists():
        click.echo(f'{_source}路径不存在.')
        exit(0)
    if (not _source.is_dir()) or (not _target.is_dir()):
        ctx.err('source和target参数必须是目录')
        exit(1)

    # 构建排除/包含列表
    ex_include_abs_list = []
    if special:
        for i in especial_file:
            ex_include_abs_list += list(_source.glob(i))
    logger.debug(f'排除/包含列表: {ex_include_abs_list}')

    # 每个source下的文件或者文件夹逐个copy到target文件夹下
    copied_file_list = []
    for root, dirs, files in os.walk(_source):
        # 将源路径中SOURCE部分替换成TARGET为后续复制所用
        # 逻辑：将current_source_root对_source取到除SOURCE部分外的相对路径
        #      在将其拼接在_target后
        # 例如：/tmp/source/A  ->  /tmp/target/A
        # _source: /tmp/source
        # _target: /tmp/target
        # 在拷贝A目录时，current_source_root: /tmp/source
        # 将/tmp/source/A 取除 /tmp/source 部分外的相对路径，即 A
        # 将_target拼接上得到/tmp/target/A
        current_source_root = pathlib.Path(root)
        current_target_root = _target / current_source_root.relative_to(
            _source)
        for d in dirs:  # 复制目录
            if (special == 'exclude') and (
                    current_source_root.joinpath(d) in ex_include_abs_list):
                logger.info(f'<{current_source_root.joinpath(d)}>在排除列表中，不拷贝。')
                continue
            elif (special == 'include') and (current_source_root.joinpath(d)
                                             not in ex_include_abs_list):
                logger.info(f'<{current_source_root.joinpath(d)}>不在包含列表中，不拷贝。')
                continue
            try:
                ctx.vlog(
                    f'正在拷贝<{current_source_root.joinpath(d)}>到<{current_target_root.joinpath(d)}>'
                )
                current_target_root.joinpath(d).mkdir(exist_ok=True)
            except Exception as e:  # 当上层目录不存在的时候会报错，这是不做处理，用来取消后续的拷贝
                ExceptionsParse(e)
        for f in files:  # 复制文件
            if (special == 'exclude') and (
                    current_source_root.joinpath(f) in ex_include_abs_list):
                logger.info(f'<{current_source_root.joinpath(f)}>在排除列表中，不拷贝。')
                continue
            elif (special == 'include') and (current_source_root.joinpath(f)
                                             not in ex_include_abs_list):
                logger.info(f'<{current_source_root.joinpath(f)}>不在包含列表中，不拷贝。')
                continue
            try:
                logger.info(
                    f'正在拷贝<{current_source_root.joinpath(f)}>到<{current_target_root.joinpath(f)}>'
                )
                shutil.copy(
                    current_source_root.joinpath(f),
                    current_target_root.joinpath(f))
                copied_file_list.append(current_source_root.joinpath(f))
            except Exception as e:  # 当上层目录不存在的时候会报错，这是不做处理，用来取消后续的拷贝
                ExceptionsParse(e)
    click.echo('copy完成^-^')
    ctx.vlog('拷贝文件清单:')
    for i in copied_file_list:
        ctx.vlog(i)
    click.echo(f'一共拷贝{len(copied_file_list)}文件')
    exit(0)


if __name__ == '__main__':
    main()
