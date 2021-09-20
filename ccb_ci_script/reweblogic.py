# -*- coding =utf-8 -*- 
import click
import paramiko

from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import log_pid
from paramiko.ssh_exception import (
    SSHException, AuthenticationException, NoValidConnectionsError
)
"""
远程执行启动脚本，重启weblogic
"""


@click.command()
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@click.option('--host', required=True, help='服务器IP')
@click.option('--username', help='服务器用户名')
@click.option('--password', help='服务器密码')
@click.option('--startscript', required=True, help='启动脚本绝对路径')
@pass_context
def main(ctx, taskid, verbose, debug, host, username, password, startscript):
    # 根据debug参数开启debug功能
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose

    def ssh_cmd(host, username, password, startscript, cmd):
        """
        远程连接服务器并执行命令
        """
        ssh = paramiko.SSHClient()
        # 建立远程免密钥文件连接
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(host, username=username, password=password, port=22)
        except AuthenticationException:
            ctx.err('远程连接认证失败！请检查账号密码是否正确！')
            exit(1)
        except NoValidConnectionsError:
            ctx.err(f'通过22号端口连接不上{host}，请检查服务器状态及端口状态！')
            exit(1)
        except SSHException:
            ctx.err('远程连接失败！')
            exit(1)
        except Exception as e:
            ExceptionsParse(e)
            exit(1)

        # 查看远程文件是否存在
        stdin, stdout, stderr = ssh.exec_command(f"ls {startscript}")  # 执行远程命令
        data = stdout.readlines()
        error = stderr.readlines()

        if error:  # 输出结果
            ctx.err('启动脚本不存在！')
            exit(1)

        stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行远程命令
        data = stdout.readlines()
        error = stderr.readlines()

        if error:  # 输出结果
            for line in error:
                line = line.strip()
                ctx.err(line)
                exit(1)
        else:
            click.echo(f'{cmd}远程命令发送成功\n')
            for line in data:
                line = line.strip()
                ctx.err(line)
        ssh.close()

    if " " in startscript:
        script = startscript.replace(" ", "\ ")
        cmd = f'sh {script}'
        ssh_cmd(host, username, password, script, cmd)
    else:
        cmd = f'sh {startscript}'
        ssh_cmd(host, username, password, startscript, cmd)


if __name__ == '__main__':
    main()
