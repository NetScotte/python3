# -*- coding=utf-8 -*-
import sys

from log import logger
"""
脚本错误类型
"""
EXCEPTIONS_DICT = {
    "E155000": "working copy配置有误，请检查相关配置。",
    "E155007": "不是一个正确的working copy",
    "E160006": "分支号在该分支上不存在。",
    "E170000": "SVN路径错误。",
    "E170001": "SVN账户权限不够。",
    "E170013": "无法连接远程仓库。",
    "E175013": "访问被拒绝，权限不足，请确认url是否正确。",
    "E215004": "SVN认证失败。",
    "E210005": "仓库不存在。",
    "E160013": "输入的版本号在目标url内不存在。请检查版本后，重新输入。",
    "WinError 5": "导出目录或文件被占用，请检查发布机目录是否被占用。",
    "WinError 145": "目录被占用，请检查发布机目录是否被占用。",
    "W170000": "分支url不存在，请检查url是否正确。",
    "E195020": "本地working copy 已不是最新版本，请先更新至最新版本。",
    "WinError 267": "目录名称无效或指定的目录不准确，请检查相关配置。",
    "E205000": "SVN分支未配置，请检查相关配置。",
    "E200009": "SVN连接失败，请检查url是否正确",
    "E731001": "SVN连接失败，请检查url是否正确。",
    "E120108": "连接被服务器关闭，请确认url是否正确。",
    "E155004": "working copy目录被锁定。",
    "E195008": "版本号输入有误",
    "WinError 10060": "由于在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。"
}


class ExceptionsParse:

    def __init__(self, e):
        self._e = e
        self._parse()

    def _parse(self):
        is_parsed = False
        for keyword, msg in EXCEPTIONS_DICT.items():
            if keyword in str(self._e):
                is_parsed = True
                logger.exception(self._e)
                print(msg, file=sys.stderr)
        if not is_parsed:
            logger.exception(self._e)
            print("遇到未知的错误，请联系管理员。")


class SvnBaseException(Exception):
    """SVN报错类型基础"""

    def __init__(self, *args, **kwargs):
        """用svn信息初始化报错"""
        super(SvnBaseException, self).__init__(*args, **kwargs)


class TimeoutError(SvnBaseException):
    """命令执行超时错误"""
    pass


class SvnAuthenticationError(SvnBaseException):
    """svn认证错误"""
    pass


class SvnRepositoryUrlError(SvnBaseException):
    """svn地址错误"""
    pass


