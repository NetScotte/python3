# -*- coding=utf-8 -*-
import subprocess
import click
import pathlib
import xml.etree.ElementTree
import dateutil.parser
import os

from urllib.parse import unquote
from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import b2s, log_pid
"""
检出jar包
"""


@click.command()
@click.option('--url', required=True, help='svn的url')
@click.option('--username', help='svn账号')
@click.option('--password', help='svn密码')
@click.option('--targetPath', required=True, help='检出路径')
@click.option('--revision', default='HEAD', help='svn版本号')
@click.option('--jar', help='jar包名')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(
    ctx, taskid, verbose, debug,
    url, username, password, targetpath, revision, jar
):
    # 根据debug参数开启debug功能
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose

    def info(url):
        """查询working copy信息
        """
        cmd = f'''svn info --non-interactive --username {username} --password {password} "{url}" --xml'''
        try:
            p = subprocess.Popen(
                cmd,
                cwd=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except Exception as e:
            ExceptionsParse(e)
            exit(1)

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
        command = f'''svn checkout --non-interactive "{url}" --username {username} --password {password} "{target_path}" --revision {revision}'''
        try:
            p = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except Exception as e:
            ExceptionsParse(e)
            exit(1)
        else:
            if stderr:
                ctx.vlog(b2s(stderr))
                ExceptionsParse(b2s(stderr))
                exit(1)
            elif p.returncode == 0:
                click.echo(f"检出成功！")
                exit(0)
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

    list_cmd = f'svn list --non-interactive "{url}" --username {username} --password {password}'
    try:
        p = subprocess.Popen(
            list_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except Exception as e:
        ExceptionsParse(e)
        exit(1)

    if stderr:
        ctx.vlog(b2s(stderr))
        ExceptionsParse(b2s(stderr))
        exit(1)
    elif (p.returncode == 0) and not stdout:
        click.echo(f"svn目录为空，不做检出！")
        exit(0)

    target_path = pathlib.Path(targetpath)
    if not target_path.exists():
        # 不存在则创建
        target_path.mkdir(parents=True)
        click.echo("路径不存在，系统自动创建该目录")
    else:
        # 判断本地是否存在jar包
        dirlist = os.listdir(target_path)
        if not dirlist:
            click.echo(f"{target_path}为空目录，直接检出{url}")
        else:
            if jar in dirlist:
                click.echo(f'{jar}本地已经存在，不做检出')
                exit(0)

            svn_info = info(target_path)
            svn_url = unquote(svn_info['url']).lower()
            if svn_url == url.lower():
                svn_checkout(url, username, password, target_path, revision)

    svn_checkout(url, username, password, target_path, revision)


if __name__ == '__main__':
    main()
