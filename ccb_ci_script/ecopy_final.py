# -*- coding=utf-8 -*-
import click
import pathlib
import os
import shutil

from cmd_context import pass_context
from common import log_pid
from log import logger
"""
将SOURCE目录下的文件拷贝到TARGET文件夹下
适用方法：
python ecopy.py SOURCE TARGET [--exclude dir1] [--exclude dir2]
注意事项：
当目标路径不存在时，自动创建。
"""


@click.command()
@click.argument('source', type=click.Path(), nargs=-1, required=True)
@click.argument('target', type=click.Path(), nargs=1)
@click.option('--exclude', '-e', multiple=True, help='排除文件/文件夹')
@click.option('--create_target', is_flag=True, help='强制创建目标目录')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='调试模式')
@pass_context
def main(ctx, source, target, exclude, create_target, taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose

    ctx.vlog(f'通配符匹配结果:{source}')

    _target = pathlib.Path(target)

    if not _target.exists():
        if create_target:
            _target.mkdir(parents=True)
        else:  # 目标不存在且没有强制创建参数
            ctx.err('目标路径文件夹不存在')
            exit(1)

    for source_ in source:  # source中有通配符则会产生tuple
        ctx.vlog(f'=================正在处理<{source_}>=================')
        _source = pathlib.Path(source_)  # 将源目转换成Path类

        # 源类型判断
        if _target.is_dir() and not _source.is_dir():  # 源为文件，不是目录
            # 构建排除列表
            exclude_abs_list = []
            if exclude:
                for i in exclude:
                    exclude_abs_list += list(_source.parent.glob(i))
            ctx.vlog(f'排除列表: {exclude_abs_list}')

            if not _source.exists():
                ctx.err('源文件不存在')
                exit(0)
            try:
                if _source not in exclude_abs_list:
                    ctx.vlog(f'正在拷贝<{_source}>到<{_target}>')
                    shutil.copy(_source, _target)
            except Exception as e:
                ctx.vlog(e)
                exit(1)

        elif _target.is_dir() and _source.is_dir():  # 源为目录

            if not _source.exists():
                click.echo(f'{_source}路径不存在.')
                exit(0)

            # 构建排除列表
            exclude_abs_list = []
            if exclude:
                for i in exclude:
                    exclude_abs_list += list(_source.glob(i))
            ctx.vlog(f'排除列表: {exclude_abs_list}')
            # 每个source下的文件或者文件夹逐个copy到target文件夹下
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
                    if current_source_root.joinpath(d) in exclude_abs_list:
                        ctx.vlog(
                            f'<{current_source_root.joinpath(d)}>在排除列表中，不拷贝。')
                        continue
                    try:
                        ctx.vlog(
                            f'正在拷贝<{current_source_root.joinpath(d)}>到<{current_target_root.joinpath(d)}>'
                        )
                        current_target_root.joinpath(d).mkdir(exist_ok=True)
                    except Exception as e:  # 当上层目录不存在的时候会报错，这是不做处理，用来取消后续的拷贝
                        ctx.vlog(e)
                for f in files:  # 复制文件
                    if current_source_root.joinpath(f) in exclude_abs_list:
                        ctx.vlog(
                            f'<{current_source_root.joinpath(f)}>在排除列表中，不拷贝。')
                        continue
                    try:
                        ctx.vlog(
                            f'正在拷贝<{current_source_root.joinpath(f)}>到<{current_target_root.joinpath(f)}>'
                        )
                        shutil.copy(
                            current_source_root.joinpath(f),
                            current_target_root.joinpath(f))
                    except Exception as e:  # 当上层目录不存在的时候会报错，这是不做处理，用来取消后续的拷贝
                        ctx.vlog(e)
    click.echo('copy完成^-^')
    exit(0)


if __name__ == '__main__':
    main()
