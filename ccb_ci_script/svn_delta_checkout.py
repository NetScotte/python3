# -*- coding: utf-8 -*-

import pathlib
import shutil
from urllib.parse import unquote
import svn.remote
import svn.exception

import click

from cmd_context import pass_context
from common import onerror, log_pid
from thread_pool import ThreadPool
from exceptions import ExceptionsParse
from svn_get_branch_earliest_revision import get_earliest_revision
from log import logger


def callback(status, result):
    """
    根据需要进行的回调函数，默认不执行。
    :param status: action函数的执行状态
    :param result: action函数的返回值
    :return:
    """
    pass


def action(
        thread_name,
        remote_client,
        target_path,
        rel_filename,
        download_rel_filename,
        end_revision,
):
    file_byte_string = remote_client.cat(download_rel_filename)
    file_dir = (target_path / rel_filename).parent
    if not file_dir.exists():
        file_dir.mkdir(parents=True, exist_ok=True)
    with open(target_path / rel_filename, "wb") as f:
        f.write(file_byte_string)


@click.command()
@click.option("--targetPath", "-t", type=click.Path(), help="导出路径")
@click.option("--revision", "-r", help="版本号，格式：<起始版本:结束版本>")
@click.option("--url", help="Svn路径")
@click.option("--username", "-u", help="svn用户名")
@click.option("--password", "-p", help="svn密码")
@click.option("--clear", is_flag=True, help="导出前清除目标路径")
@click.option("--continue", "go_on", is_flag=True, help="无文件导出时继续执行")
@click.option("--taskid")
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option("--debug", is_flag=True, help="调试模式")
@pass_context
def main(ctx, targetpath, revision, url, username, password, clear, go_on,
         taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    thread_num = 10
    logger.info('线程池大小:%s', thread_num)
    # 版本号参数解析
    start_revision, *end_revision = revision.split(":")
    try:
        start_revision = int(start_revision)
    except ValueError as e:
        ctx.err("非法的版本号输入")
        exit(1)
    if not end_revision:
        end_revision = "HEAD"
    elif end_revision[0].upper() == "HEAD":
        end_revision = "HEAD"
    else:
        try:
            end_revision = int(end_revision[0])
        except Exception as e:
            ctx.err("非法的版本号输入")
            exit(1)
    # 检查分支最小版本号
    try:
        if int(start_revision) < get_earliest_revision(url, username,
                                                       password):
            start_revision = get_earliest_revision(url, username, password)
            ctx.vlog(
                f'''输入的分支号小于该分支创建时的基板号（{get_earliest_revision(url, username, password)}）'''
            )
    except svn.exception.SvnException as e:
        ExceptionsParse(e)
        exit(1)

    target_path = pathlib.Path(targetpath)
    if not target_path.exists():
        # 不存在则创建
        target_path.mkdir(parents=True)
    else:
        if clear:  # 已存在且有clear参数则清理目录。
            try:
                shutil.rmtree(target_path, onerror=onerror)
            except Exception as e:
                ExceptionsParse(e)
                ctx.err("请查看发布机文件占用情况,建议关闭文件窗口。再有问题请联系管理员.")
            else:
                try:
                    target_path.mkdir(parents=True)
                except Exception as e:
                    ExceptionsParse(e)
                click.echo(f"清理{target_path}成功。")

    remote_client = svn.remote.RemoteClient(
        url, username=username, password=password)
    remote_client
    # 获取diff_list
    try:
        click.echo("正在比较版本...")
        diff_list = remote_client.diff_summary(start_revision, end_revision)
    except svn.exception.SvnException as e:
        ExceptionsParse(e)
        exit(1)

    # 获取版本号
    last_commit_revision = remote_client.info()["commit#revision"]
    last_revision = remote_client.info()["entry#revision"]

    added, modified, delete = 0, 0, 0
    pool = ThreadPool(thread_num)
    for i in diff_list:
        _path = unquote(i["path"], "utf-8", errors="replace")
        _kind = i["kind"]
        _item = i["item"]
        click.echo(f"""{_item}\t{_path}""")
        if (_kind == "file") and (_item == "deleted"):
            delete += 1
        if (_kind == "file") and (_item == "added" or _item == "modified"):
            if _item == "added":
                added += 1
            elif _item == "modified":
                modified += 1
            rel_filename = _path.replace(remote_client.url + "/", "")
            download_rel_filename = rel_filename + f"@{end_revision}"
            pool.put(
                action,
                (
                    remote_client,
                    target_path,
                    rel_filename,
                    download_rel_filename,
                    end_revision,
                ),
                callback,
            )
    pool.close()
    click.echo(f"新增:{added}, 修改:{modified}, 删除:{delete}")
    click.echo(f"本次变更文件数量: {added+modified}")
    click.echo(f"分支最新版本号: {last_commit_revision}")
    click.echo(f"仓库最新版本号: {last_revision}")
    click.echo("成功获取.")


if __name__ == "__main__":
    import datetime

    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    click.echo(f"耗时：{end-start}")
# python3 svn_delta_checkout.py --url svn://svn@172.16.159.129/ccb/branches/branch002 --targetPath /Users/abin/code/uw/ccb_ci_script/ccb/trunk --revision 8:17 --username svn --password svn

