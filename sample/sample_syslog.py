# -*- coding: utf-8 -*-
"""
功能：
设计：
备注：
时间：
"""
import logging
import logging.handlers as lh
import syslog


def sample_logging_syslog():
    logger = logging.getLogger("sample")
    logger.addHandler(lh.SysLogHandler(address="/dev/log"))
    logger.setLevel(logging.DEBUG)
    logger.info("this is a message from python")


def sample_syslog():
    syslog.syslog("this is from python")


if __name__ == "__main__":
    # sample_syslog()
    sample_logging_syslog()