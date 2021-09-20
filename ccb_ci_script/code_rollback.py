# -  *  - coding = utf-8 -  *  - 
import click
import paramiko
import sqlite3

import pathlib
from log import logger
from exceptions import ExceptionsParse
from cmd_context import pass_context
from common import log_pid
from paramiko.ssh_exception import (
    SSHException, AuthenticationException, NoValidConnectionsError
)
"""
tar包
"""


@click.command()
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@click.option('--host', required=True, help='服务器IP')
@click.option('--username', help='服务器用户名')
@click.option('--password', help='服务器密码')
@click.option('--targetpath', required=True, help='应用路径')
@pass_context
def main(ctx, taskid, verbose, debug, host, username, password, targetpath):
    # 根据debug参数开启debug功能
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose

    def select_filename(host, targetpath):
        """查询代码包名"""
        try:
            logger.debug(f'正在链接代码包名数据库{PACKAGE_DB}')
            conn = sqlite3.connect(str(PACKAGE_DB.resolve()))
            cur = conn.cursor()
        except Exception:
            logger.exception('链接数据库异常')
            exit(1)

        try:
            select_tb_cmd = f'''SELECT FILENAME,STATUS from PACKAGE_NAME WHERE HOST="{host}" AND TARGETPATH="{targetpath}";'''
            cur.execute(select_tb_cmd)
            logger.debug('数据查询成功')
        except Exception:
            logger.exception('数据查询失败')
            exit(1)

        info_list = cur.fetchall()
        if not info_list:
            ctx.err(f'数据查询失败，数据库中无{targetpath}代码包数据')
            exit(1)
        else:
            filename = info_list[0][0]
            status = info_list[0][1]
            return filename, status
        conn.close()

    def ssh_cmd(host, username, password, targetpath, cmd, filename):
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
            
        sftp = ssh.open_sftp()
        try:  # 查看远程文件是否存在
            sftp.stat(filename)
        except IOError:
            ctx.err(f'"{filename}"不存在！')
            exit(1)

        click.echo(f'将要解压"{filename}"~~~~~~')
        stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行命令
        data = stdout.read()
        error = stderr.read()
        if error:  # 输出打包结果
            ctx.err(error)
            exit(1)
        else:
            click.echo(f'"{filename}"解压成功\n')
            ctx.err(data)
        ssh.close()

    PACKAGE_DB = pathlib.Path(__file__).parent.joinpath('package.db')
    file_name, status = select_filename(host, targetpath)
    if status != 'success':
        # 查看包状态，若不为success则不进行解压，并且删除服务器上不完整的包
        click.echo(f'{file_name}包不完整，不进行解压')
        rm_ssh = paramiko.SSHClient()
        rm_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            rm_ssh.connect(host, username=username, password=password, port=22)
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

        rm_sftp = rm_ssh.open_sftp()
        try:  # 查看远程文件是否存在
            rm_sftp.stat(file_name)
        except IOError:
            logger.error(f'"{file_name}"不存在！')
            exit(1)
        rm_sftp.remove(file_name)
        rm_ssh.close()
        exit(1)

    # 解压包
    cmd = f'tar -Pxf "{file_name}"'
    ssh_cmd(host, username, password, targetpath, cmd, file_name)


if __name__ == '__main__':
    main()
