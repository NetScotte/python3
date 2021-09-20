# -*- coding=utf-8 -*-
import click
import sys
import os
import re

from log import logger


class Context(object):

    def __init__(self):
        self.debug = False
        self.verbose = False
        self.home = os.getcwd()

    def err(self, msg, *args, **kwargs):
        """Logs a message to stderr."""
        click.echo(msg, file=sys.stderr, *args, **kwargs)

    def vlog(self, msg, *args, **kwargs):
        """Logs a message to stderr only if verbose is enabled."""
        # TODO: 为了兼容之前脚本中的debug参数，所以debug和verbose都可使用
        if self.debug or self.verbose:
            click.echo(msg, *args, **kwargs)

    def check_param(self, param, regex_list, exact_list):
        """检查输入参数
        使用方法：
        1. 可以传入list，来定义检查黑名单
        2. regex_list是普通匹配，exact_list是精确匹配
        """
        logger.debug('普通正则列表:%s, 精确匹配列表:%s', regex_list, exact_list)
        _kwargs = {}
        try:
            for k, v in param.items():
                _kwargs.setdefault(k, str(v))
        except Exception as e:
            logger.exception(f"参数<{v.__class__}: {v}>无法校验合法性")

        for ban in regex_list:
            pattern = re.compile(ban, re.I)
            for k, v in _kwargs.items():
                if pattern.search(v):
                    click.echo(f"[{v}]为非法参数!", file=sys.stderr)
                    exit(1)

        for ban in exact_list:
            pattern = re.compile(ban, re.I)
            for k, v in _kwargs.items():
                if pattern.fullmatch(v):
                    click.echo(f"[{v}]为非法参数!", file=sys.stderr)
                    exit(1)


pass_context = click.make_pass_decorator(Context, ensure=True)
