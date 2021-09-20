# -*- coding=utf-8 -*-
import subprocess
import click
import pathlib
import shutil
import xml.etree.ElementTree
import dateutil.parser
import os

from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import b2s, onerror, log_pid
"""
svn检出
"""


@click.command()
@click.option('--url', required=True, help='svn的url')
@click.option('--username', help='svn账号')
@click.option('--password', help='svn密码')
@click.option('--targetPath', required=True, help='检出路径')
@click.option('--revision', default='HEAD', help='svn版本号')
@click.option('--clear', is_flag=True, help='清空targetPath')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, taskid, verbose, debug, url, username, password, targetpath, revision, clear):
    # 根据debug参数开启debug功能
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose

    def info(svn_url):
        """查询working copy信息
        """
        cmd = f'svn info --non-interactive  --username {username} --password {password} "{svn_url}" --xml'
        p = subprocess.Popen(
            cmd,
            cwd=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stderr:
            ctx.vlog(b2s(stderr))
            ExceptionsParse(b2s(stderr))
            exit(1)
        else:
            entry = xml.etree.ElementTree.fromstring(stdout)
            return {
                'url':
                entry.find('entry/url').text,
                'rel_url':
                entry.find('entry/relative-url').text,
                'root':
                entry.find('entry/repository/root').text,
                'revision':
                entry.find('entry').attrib['revision'],
                'last_changed_author':
                entry.find('entry/commit/author').text,
                'last_changed_rev':
                entry.find('entry/commit').attrib['revision'],
                'last_changed_date':
                dateutil.parser.parse(entry.find('entry/commit/date').text),
            }

    def svn_checkout(url, username, password, target_path, revision):
        """检出
        """
        # 查看url是否合法
        svn_info = info(url)
        svn_url = svn_info['url']
        # 执行检出命令
        if svn_url == url:
            command = f'svn checkout --non-interactive "{url}" --username {username} --password {password} "{target_path}" --revision {revision}'
            p = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            stdout, stderr = p.communicate()
            if p.returncode == 0:
                wc_info = info(target_path)
                wc_bran = wc_info['rel_url'][2:]
                wc_rev = wc_info['last_changed_rev']
                click.echo(f"{wc_bran}检出成功,{wc_bran}检出版本号为{wc_rev}")
                exit(0)
            else:
                ExceptionsParse(b2s(stderr))
                exit(1)

    # 判断revision的值
    if revision != 'HEAD':
        try:
            if int(revision) < 0:
                click.echo("请输入版本号大于0！")
                exit(1)
        except ValueError:
            click.echo("版本号输入有误")
            exit(1)
        except Exception as e:
            ExceptionsParse(e)
            exit(1)

    target_path = pathlib.Path(targetpath)
    if not target_path.exists():
        # 不存在则创建
        target_path.mkdir(parents=True)
        click.echo("路径不存在，系统自动创建该目录")
    else:
        if clear:  # 已存在且有clear参数则清理目录。
            try:
                shutil.rmtree(target_path, onerror=onerror)
            except Exception as e:
                ExceptionsParse(e)
                ctx.err("请查看发布机文件占用情况,建议关闭文件窗口。再有问题请联系管理员.")
                exit(1)
            else:
                try:
                    target_path.mkdir(parents=True)
                except Exception as e:
                    ExceptionsParse(e)
                    exit(1)
                click.echo(f"清理{target_path}成功。")
        else:  # 查看workingcopy状态
            dirlist = os.listdir(target_path)
            if not dirlist:
                click.echo(f"{target_path}为空目录，直接检出{url}")
                svn_checkout(url, username, password, target_path, revision)
            else:
                wc_info = info(target_path)
                # 执行更新命令
                wc_url = wc_info['url']
                if wc_url == url:
                    update_cmd = f'svn update --non-interactive --username {username} --password {password} "{target_path}" --revision {revision}'
                    p = subprocess.Popen(
                        update_cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                    stdout, stderr = p.communicate()
                    if p.returncode == 0:
                        wc_info = info(target_path)
                        wc_bran = wc_info['rel_url'][2:]
                        wc_rev = wc_info['last_changed_rev']
                        click.echo(f"working copy已存在并更新成功，{wc_bran}检出版本号为{wc_rev}")
                        exit(0)
                    else:
                        ExceptionsParse(b2s(stderr))
                        exit(1)
    svn_checkout(url, username, password, target_path, revision)


if __name__ == '__main__':
    main()
