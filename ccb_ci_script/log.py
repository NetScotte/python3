# -*- coding=utf-8 -*-
import logging
import logging.handlers
import sys
from pathlib import Path


class MyLogger(logging.getLoggerClass()):

    # 日志目录
    LOGFILE_DIR = Path(__file__).parent.joinpath("logs")
    if not LOGFILE_DIR.exists():
        LOGFILE_DIR.mkdir()
    # 日志文件路径
    LOGFILE_PATH = LOGFILE_DIR.joinpath("shepherd_scripts")

    # =============== Formatter ==================
    # 简略格式，用于console输出，例如：
    # 2018/06/21 14:40:47 |INFO    | [模块:log] info msg
    # 2018/06/21 14:40:47 |WARNING | [模块:log] warn msg
    # 2018/06/21 14:40:47 |ERROR   | [模块:log] error msg
    # 2018/06/21 14:40:47 |CRITICAL| [模块:log] critial msg
    _brief = logging.Formatter(
        fmt="%(asctime)s |%(levelname)-8s| [模块:%(module)s] %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S")

    # 详细格式，用于输出到文件，例如：
    # 2018/06/21 14:51:1529563880 [ERROR] [模块:log][函数:<module>][行号:62][pid:38849] error msg
    # 2018/06/21 14:51:1529563880 [CRITICAL] [模块:log][函数:<module>][行号:63][pid:38849] critial msg
    # 2018/06/21 14:51:1529563880 [ERROR] [模块:log][函数:<module>][行号:72][pid:38849] division by zero
    _detail = logging.Formatter(
        fmt=
        "%(asctime)s [%(levelname)s] [模块:%(module)s][函数:%(funcName)s][行号:%(lineno)d][pid:%(process)d] %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    # =============== Handler ==================
    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(_brief)
    console_handler.setLevel(level=logging.DEBUG)

    # 文件输出
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=LOGFILE_PATH, when="D", backupCount=0, encoding="utf-8")
    file_handler.setLevel(level=logging.ERROR)
    file_handler.setFormatter(_detail)

    def __init__(self, *args, **kwargs):
        super(MyLogger, self).__init__(*args, **kwargs)
        self.addHandler(self.file_handler)

    def debug_on(self):
        """开启debug，将debug日志输出到console"""
        self.addHandler(self.console_handler)

    def debug_off(self):
        """关闭debug"""
        self.removeHandler(self.console_handler)


logger = MyLogger(__name__)
logger.setLevel(level=logging.DEBUG)

if __name__ == "__main__":
    # 测试log用例
    logger.debug("debug msg")
    logger.info("info msg")
    logger.warn("warn msg")
    logger.error("error msg")
    logger.critical("critial msg")

    def div(x, y):
        1 / 0
        return x / y

    try:
        a = div(1, 1)
    except ZeroDivisionError as e:
        logger.exception('错误类型:%s, 错误信息:%s', e.__class__, e)
