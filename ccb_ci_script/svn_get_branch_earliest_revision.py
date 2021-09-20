# -*- coding=utf-8 -*-
import svn.remote
from svn.exception import SvnException


def get_earliest_revision(url, username, password):
    r = svn.remote.RemoteClient(url, username=username, password=password)
    try:
        earliest_log = list(r.log_default(stop_on_copy=True))[-1]
    except SvnException as e:
        raise
    earliest_revision = earliest_log.revision
    return int(earliest_revision)
