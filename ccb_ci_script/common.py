# -*- coding=utf-8 -*-
import contextlib
import tempfile
import os
import shutil
import sqlite3
import platform
import codecs
import psutil
from pathlib import Path

from exceptions import ExceptionsParse
from log import logger


@contextlib.contextmanager
def isolated_filesystem(suffix=None, prefix=None):
    """这个上下文管理器可以创建一个临时文件夹，
    并且将当前目录切换到这个独立的文件系统中
    """
    cwd = os.getcwd()
    t = tempfile.mkdtemp(suffix=suffix, prefix=prefix)
    os.chdir(t)
    try:
        yield t
    finally:
        os.chdir(cwd)
        try:
            shutil.rmtree(t)
        except (OSError, IOError):
            pass


def b2s(bytes_string):
    """将bytes字符串根据当前系统的编码转成utf-8字符串"""
    if not isinstance(bytes_string, bytes):
        raise TypeError('字符串必须是bytes类型')
    return {
        'Windows': lambda s: codecs.decode(s, encoding='gbk'),
        'Linux': lambda s: codecs.decode(s, encoding='utf-8'),
        'Darwin': lambda s: codecs.decode(s, encoding='utf-8')
    }.get(platform.system(),
          lambda s: codecs.decode(s, encoding='utf-8'))(bytes_string)


PID_DB = Path(__file__).parent.joinpath('pid.db')


def log_pid(task_id):
    """记录主进程pid"""
    p = psutil.Process(os.getpid())
    try:
        logger.debug(f'正在链接pid数据库({PID_DB})')
        conn = sqlite3.connect(str(PID_DB.resolve()))
        try:
            create_tb_cmd = '''CREATE TABLE IF NOT EXISTS PID (PID INTEGER, TASK_ID TEXT, CREATE_TIME REAL);'''
            logger.debug(f'创建表成功或已存在')
            conn.execute(create_tb_cmd)
        except Exception:
            logger.exception('创建表失败')
        else:
            try:
                insert_dt_cmd = f'''INSERT INTO PID (PID,TASK_ID,CREATE_TIME) VALUES ("{os.getpid()}", "{task_id}", "{p.create_time()}");'''
                conn.execute(insert_dt_cmd)
                logger.debug('插入数据:  PID:%s Task_id:%s CREATE_TIME:%s', os.getpid(), task_id, p.create_time())
            except Exception:
                logger.exception('插入数据异常')
        finally:
            conn.commit()
            conn.close()
    except Exception:
        logger.exception('链接数据库异常')


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.
    Usage: ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        try:
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        except Exception:
            raise
    else:
        raise


if __name__ == "__main__":
    log_pid('asdfsdf')
