# -*- coding=utf-8 -*-
import functools
import logging


def log_args(func):
    logger = logging.getLogger(func.__name__)

    @functools.wraps(func)
    def wapper(*args, **kwargs):
        logger.debug(f'{args}{kwargs}')
        return func(*args, **kwargs)

    return wapper
