# -*- coding=utf-8 -*-
import os
import signal
import click
import platform
import sqlite3

from exceptions import ExceptionsParse
from kill_log import logkill
from common import PID_DB
"""杀死pid进程，以及其子进程"""


@click.command()
@click.option('--taskid', type=str, help='子任务id')
def main(taskid):
    logkill.debug_on()
    for i in range(3):
        try:
            logkill.info(f'正在链接pid数据库({PID_DB})')
            conn = sqlite3.connect(str(PID_DB.resolve()))
            cursor = conn.cursor()
        except Exception as e:
            ExceptionsParse(e)
            logkill.exception('操作数据库异常')
        else:
            cursor.execute('select * from PID where TASK_ID=? order by CREATE_TIME desc', (taskid,))
            values = cursor.fetchall()
            type(values)
            if not values:
                logkill.warn('没有找到taskid:%s', taskid)
                conn.close()
                exit(1)
            else:
                for j in values:
                    pid = j[0]
                    try:
                        if platform.system() == 'Linux' or platform.system() == 'Darwin':
                            os.killpg(pid, signal.SIGKILL)
                            logkill.info(f'{pid}进程已经终止.')
                        elif platform.system() == 'Windows':
                            os.system(f'TASKKILL /F /PID {pid} /T')
                            logkill.info(f'{pid}进程已经终止.')
                    except Exception as e:
                        ExceptionsParse(e)

    try:
        cursor.execute(f'''DELETE from PID where TASK_ID='{taskid}';''')
    except Exception as e:
        ExceptionsParse(e)
        logkill.exception('删除数据失败')
    else:
        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
