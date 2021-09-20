# -*- coding=utf-8 -*-
import click
import subprocess
import xml.etree.ElementTree
from collections import namedtuple
import dateutil.parser

from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import log_pid, b2s
"""
svn merge
"""


class SvnException(Exception):
    pass


CONFLICT_CHOICE = [
    'working',
    'base',
    'mine-conflict',
    'theirs-conflict',
    'mine-full',
    'theirs-full',
]


@click.command()
@click.option('--mergeBranch', '-m', required=True, help='源分支')
@click.option(
    '--targetPath',
    '-t',
    type=click.Path(exists=True),
    required=True,
    help='目标分支WorkingCopy')
@click.option(
    '--conflictChoice',
    '-c',
    type=click.Choice(CONFLICT_CHOICE),
    default='theirs-full',
    help="自动解决冲突动作。")
@click.option('--username', '-u', help='svn账号')
@click.option('--password', '-p', help='svn密码')
@click.option('--resolve', is_flag=True, help='解决冲突开关')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, mergebranch, targetpath, conflictchoice, username, password, resolve,
         taskid, verbose, debug):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose

    def run_command(subcommand,
                    args,
                    username=username,
                    password=password,
                    wd=None,
                    realtime_output=False):
        """执行命令通用方法

        :param subcommand: svn子命令
        :type subcommand: string
        :param args: svn自命令参数
        :type args: list
        :param username: svn账号
        :param username: string, optional
        :param password: svn密码
        :param password: string, optional
        :param wd: 命令执行目录
        :param wd: string, optional,默认:None
        :param realtime_output: 是否实时输出
        :param realtime_output: boolean, 默认: False
        :return: 命令执行结果和出错stdout, stderr
        :rtype: tuple
        """

        cmd = ['svn', '--non-interactive']
        if username is not None and password is not None:
            cmd += [
                '--username', username, '--password', password,
                '--no-auth-cache'
            ]
        cmd += [subcommand] + args
        logger.debug('执行命令：%s', cmd)
        p = subprocess.Popen(
            cmd,
            cwd=wd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        stdout = ''
        stderr = None
        if realtime_output:
            while p.poll() is None:
                line = p.stdout.readline()
                line = b2s(line)
                if line:
                    click.echo(line.strip())
                    stdout += line
            else:
                p.stdout.close()
                if p.stderr:
                    stderr = b2s(p.stderr.read())
                    p.stderr.close()
        else:
            stdout, stderr = p.communicate()

        if p.returncode != 0:
            raise SvnException("命令执行错误({}): {}".format(p.returncode,
                                                       b2s(stdout)))
        return stdout, stderr

    Status_Entry = namedtuple('Status_Entry',
                              ['name', 'type', 'tree_conflicted', 'revision'])

    def status(targetpath):
        """查看workingcopy的状态

        :param targetpath: workingcopy路径
        :type targetpath: string
        """

        st_stdout, st_stderr = run_command(
            subcommand='status', args=[targetpath, '--xml'])
        root = xml.etree.ElementTree.fromstring(st_stdout)

        list_ = root.findall('target/entry')
        for entry in list_:
            entry_attr = entry.attrib
            name = entry_attr['path']

            wcstatus = entry.find('wc-status')
            wcstatus_attr = wcstatus.attrib

            change_type_raw = wcstatus_attr['item']
            tree_conflicted = True if wcstatus_attr.get(
                'tree-conflicted') else False

            revision = wcstatus_attr.get('revision')
            if revision is not None:
                revision = int(revision)

            yield Status_Entry(
                name=name,
                type=change_type_raw,
                tree_conflicted=tree_conflicted,
                revision=revision)

    def info(svn_url):
        """查看svn仓库info

        :param svn_url: svn地址或者wc地址
        :type svn_url: string
        :return: info信息
        :rtype: dict
        """

        st_stdout, st_stderr = run_command(
            subcommand='info', args=[svn_url, '--xml'])
        entry = xml.etree.ElementTree.fromstring(st_stdout)
        return {
            'url':
            entry.find('entry/url').text,
            'rel_url':
            entry.find('entry/relative-url').text,
            'root':
            entry.find('entry/repository/root').text,
            'revision':
            entry.find('entry/repository/root').text,
            'last_changed_author':
            entry.find('entry/commit/author').text,
            'last_changed_rev':
            entry.find('entry/commit').attrib['revision'],
            'last_changed_date':
            dateutil.parser.parse(entry.find('entry/commit/date').text),
        }

    # 更新workingcopy
    try:
        run_command(
            subcommand='update',
            wd=targetpath,
            args=[],
        )
    except SvnException as e:
        ExceptionsParse(e)
        exit(1)

    # 合并前获取分支信息
    try:
        mb_info = info(mergebranch)
    except SvnException as e:
        ExceptionsParse(e)
        exit(1)
    mb_rel_url = mb_info['rel_url'][2:]
    mb_revision = mb_info['last_changed_rev']

    # 合并
    try:
        run_command(
            subcommand='merge',
            args=[mergebranch, targetpath, '--accept', 'postpone'],
            realtime_output=verbose)
    except SvnException as e:
        ExceptionsParse(e)
        exit(1)

    # 分析合并结果(分析冲突)
    tree_conflicted_list = []
    file_conflicted_list = []
    merge_file_list = []
    try:
        for i in status(targetpath):
            if i.type == 'unversioned':
                continue
            merge_file_list.append(i)
            if i.tree_conflicted:
                tree_conflicted_list.append(i)
            if i.type == 'conflicted':
                file_conflicted_list.append(i)
    except SvnException as e:
        ExceptionsParse(e)
        exit(1)

    # 输出树冲突文件列表
    if tree_conflicted_list:
        click.echo('树冲突文件列表[Tree Conflict list]'.center(35, '='))
        for i in tree_conflicted_list:
            click.echo(f'{i.name}')
        else:
            # 打印空行，与后面内容分开
            click.echo('')
    else:

        # 输出冲突文件列表
        if file_conflicted_list:
            click.echo('冲突文件列表[Conflict list]'.center(35, '='))
            for i in file_conflicted_list:
                click.echo(f'{i.name}')
            else:
                # 打印空行，与后面内容分开
                click.echo('')

        # 输出合并文件列表
        if merge_file_list:
            logger.debug(merge_file_list)
            if len(merge_file_list) == 1 and merge_file_list[0].type == 'normal':
                click.echo(f'合并源分支： {mb_rel_url}')
                click.echo(f'分支最新版本号： {mb_revision}')
                click.echo('本次没有文件需要合并')
                exit(0)
            click.echo('合并文件列表'.center(35, '='))
            for i in merge_file_list:
                click.echo(f'{i.type.ljust(15)} {i.name}')
            else:
                # 打印空行，与后面内容分开
                click.echo('')
        else:
            click.echo('本次没有文件需要合并')
            exit(0)

    # 当tree conflict回退
    if tree_conflicted_list:
        try:
            run_command(
                subcommand='revert',
                args=[targetpath, '--recursive'],
            )
            click.echo('由于Tree Conflict合并失败。')
        except SvnException as e:
            ExceptionsParse(e)
        exit(1)
    if resolve:
        # 当file conflict回退
        if file_conflicted_list:
            try:
                run_command(
                    subcommand='revert',
                    args=[targetpath, '--recursive'],
                )
                click.echo('由于File Conflict合并失败。')
            except SvnException as e:
                ExceptionsParse(e)
            exit(1)
        else:
            try:
                # 解决冲突
                run_command(
                    subcommand='resolve',
                    args=[targetpath, '--accept', conflictchoice, '--recursive'],
                )

                # 获取被合并分支信息
                t_info = info(targetpath)
                t_rel_url = t_info['rel_url'][2:]

                # 提交
                commit_comment = f'从 {mb_rel_url}@{mb_revision} 分支合并至 {t_rel_url} 上'
                run_command(
                    subcommand='commit',
                    args=['-m', commit_comment],
                    wd=targetpath,
                )

                # 重新获取目标分支合并后的信息
                t_info_after_merge = info(targetpath)
                t_revision_after_merge = t_info_after_merge['last_changed_rev']

                # 输出
                click.echo(f'仓库地址：{t_info["root"]}')
                click.echo(f'合并源分支： {mb_rel_url}')
                click.echo(f'分支最新版本号： {mb_revision}')
                click.echo(f'{t_rel_url} 目标分支合并后版本号：{t_revision_after_merge}')
                click.echo('合并成功')
            except SvnException as e:
                ExceptionsParse(e)
                ctx.err('合并失败。')

                # 回退
                run_command(
                    subcommand='revert',
                    args=[targetpath, '--recursive'],
                )
                exit(1)


if __name__ == '__main__':
    main()
