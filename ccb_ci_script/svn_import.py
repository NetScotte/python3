# -*- coding=utf-8 -*-
import pathlib
import subprocess

import click

from cmd_context import pass_context
from exceptions import ExceptionsParse
from common import b2s, log_pid
from log import logger
"""
导入文件到svn指定路径下
"""


@click.command()
@click.option("--username", help="svn账号")
@click.option("--password", help="svn密码")
@click.option("--url", help="分支url")
@click.option("--path", help="导入文件路径")
@click.option("--filename", help="导入文件文件名")
@click.option("--taskid")
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option("--debug", is_flag=True, help='调试模式')
@pass_context
def main(ctx,
         username,
         password,
         url,
         path,
         filename,
         verbose,
         debug,
         taskid):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    """上传文件至svn"""
    url += '/' if not url.endswith('/') else ''
    if not filename or not path:
        ctx.err("导入文件路径或文件名参数未被正确填写。")
        exit(1)
    else:
        filepath = pathlib.Path(path).joinpath(filename)
    try:
        if not filepath.exists():
            ctx.err(f"{filepath}不存在。")
            exit(1)
        if filepath.is_dir():
            ctx.err(f"{filepath}为非法路径。仅单个文件路径是合法的。")
            exit(1)
    except Exception as e:
        ExceptionsParse(e)
        exit(1)

    # 检查文件在svn上是否存在
    list_command = f'svn list --non-interactive --username {username} --password {password} "{url}{filename}"'
    list_p = subprocess.Popen(
        list_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    l_stdout, l_stderr = list_p.communicate()
    if (list_p.returncode == 0) and l_stdout:
        # 删除svn上已存在的文件
        del_command = f'svn del --non-interactive --username {username} --password {password} "{url}{filename}" -m "Delete {filename}"'
        del_p = subprocess.Popen(
            del_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        del_stdout, del_stderr = del_p.communicate()
        if del_p.returncode != 0:
            ExceptionsParse(b2s(del_stderr))
            exit(1)
    # 上传文件到svn
    import_command = f'svn import "{filename}" --non-interactive --username {username} --password {password} "{url}{filename}" -m "Add {filename}"'
    import_p = subprocess.Popen(
        import_command,
        cwd=path,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    i_stdout, i_stderr = import_p.communicate()
    if i_stderr:
        ctx.vlog(b2s(i_stderr))
        ExceptionsParse(b2s(i_stderr))
        ctx.err("上传文件失败!")
        exit(1)
    else:
        click.echo(f"上传{filename}文件成功!")
        exit(0)


if __name__ == '__main__':
    main()
