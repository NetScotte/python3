# -*- coding =utf-8 -*- 
import click
import datetime
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

    def log_replace(host, targetpath, filename, status):
        """插入数据"""
        try:
            logger.debug(f'即将插入或更新数据。HOST:{host} TARGETPATH:{targetpath} FILENAME:{filename} STATUS:{status}')
            insert_cmd = f'''REPLACE INTO PACKAGE_NAME(HOST,TARGETPATH,FILENAME,STATUS) VALUES("{host}","{targetpath}","{filename}","{status}");'''
            conn.execute(insert_cmd)
            logger.debug('插入数据成功')
        except Exception:
            logger.exception('插入数据失败')
            exit(1)
        finally:
            conn.commit()

    def ssh_cmd(host, username, password, targetpath, cmd):
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

        # 判断目录是否存在，是否为空
        du_stdin, du_stdout, du_stderr = ssh.exec_command(f'du -s {targetpath}')
        du_data = du_stdout.read()
        du_err = du_stderr.read()
        if du_err:
            ctx.err(du_err)
            exit(1)
        else:
            if int(du_data.decode().split()[0]) == 4:
                ctx.err('目录为空！不进行打包')
                exit(1)

        stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行打包命令
        data = stdout.read()
        error = stderr.read()
        if error:  # 输出打包结果
            ctx.err(error)
            exit(1)
        else:
            click.echo(f'{targetpath}打包成"{filename}"成功\n')
            ctx.err(data)
        ssh.close()

    PACKAGE_DB = pathlib.Path(__file__).parent.joinpath('package.db')
    timestamp = datetime.date.today().strftime("%Y%m%d")
    filename = targetpath + timestamp + '.tar'  # 拼接包名，"目录名+年月日.tar"
    cmd = f'tar -Pcf "{filename}" "{targetpath}"'

    # 链接数据库
    try:
        logger.debug(f'正在链接包名数据库{PACKAGE_DB}')
        conn = sqlite3.connect(str(PACKAGE_DB.resolve()))
    except Exception:
        logger.exception('链接数据库异常')
        exit(1)

    # 创建表
    try:
        create_tb_cmd = '''CREATE TABLE IF NOT EXISTS PACKAGE_NAME(
            HOST TEXT NOT NULL,
            TARGETPATH TEXT NOT NULL,
            FILENAME TEXT,
            STATUS TEXT,
            PRIMARY KEY(HOST, TARGETPATH));'''
        conn.execute(create_tb_cmd)
        logger.debug(f'创建表成功或已存在')
    except Exception:
        logger.exception('创建表失败')
        exit(1)

    # 插入数据，状态为待打包
    log_replace(host, targetpath, filename, status='pending')
    ssh_cmd(host, username, password, targetpath, cmd)
    log_replace(host, targetpath, filename, status='success')  # 更改状态为成功
    conn.close()


if __name__ == '__main__':
    main()
