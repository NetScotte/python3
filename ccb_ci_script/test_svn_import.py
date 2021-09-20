# -*- coding=utf-8 -*-
import pytest
from click.testing import CliRunner
from svn_import import main as app

test_data = [
    # 一般情况
    ('dir', '1.txt', 'svn://localhost/proj1/trunk', 'huangxiaojun',
     'huangxiaojun', "上传%s文件成功!\n"),
    # svn上已存在
    ('dir', '1.txt', 'svn://localhost/proj1/trunk', 'huangxiaojun',
     'huangxiaojun', "上传%s文件成功!\n"),
    # 文件名和目录中有中文
    ('中文', '中文测试文件.txt', 'svn://localhost/proj1/trunk', 'huangxiaojun',
     'huangxiaojun', "上传%s文件成功!\n"),
    # 有空格
    ('空格 目录', '空格 文件.txt', 'svn://localhost/proj1/trunk', 'huangxiaojun',
     'huangxiaojun', "上传%s文件成功!\n"),
    # 不存在的svn地址
    ('空格 目录', '空格 文件.txt', 'svn://localhost/proj1/trunk/不存在', 'huangxiaojun',
     'huangxiaojun', "上传%s文件成功!\n"),
    # 仓库不存在
    ('dir', '1.txt', 'svn://localhost/undefinded/trunk', 'huangxiaojun',
     'huangxiaojun', "仓库不存在。\n"),
    # 只读权限svn账号
    ('dir', '1.txt', 'svn://localhost/proj1/trunk', 'ro', 'ro',
     "SVN账户权限不够。\n"),
    # 文件名中有符合windows规则
    ('dir', '含有&()_+[]{},;~.txt', 'svn://localhost/proj1/trunk',
     'huangxiaojun', 'huangxiaojun', "上传%s文件成功!\n"),
    # 文件名为空
    ('dir', '', 'svn://localhost/proj1/trunk', 'huangxiaojun', 'huangxiaojun',
     "导入文件路径或文件名参数未被正确填写。\n"),
]


@pytest.mark.parametrize(
    "abspath, filename, svnurl, svn_username, svn_password, excepted",
    test_data)
def test_svn_import(abspath, filename, svnurl, svn_username, svn_password,
                    excepted, tmpdir):
    p = tmpdir.mkdir(abspath)
    try:
        f = p.join(filename)
        f.write('This is unit test file.')
    except:
        print("创建文件失败")
    runner = CliRunner()
    result = runner.invoke(app, [
        '--username', svn_username, '--password', svn_password, '--url',
        svnurl, '--path', p, '--filename', filename, '--debug'
    ])
    if '%s' in excepted:
        excepted %= filename
    assert excepted in result.output


def test_svn_import_with_dir(tmpdir):
    # 上传文件夹
    tmpdir.mkdir('dir1')
    runner = CliRunner()
    result = runner.invoke(app, [
        '--username', 'huangxiaojun', '--password', 'huangxiaojun', '--url',
        'svn://localhost/proj1/trunk', '--path', tmpdir, '--filename', 'dir1',
        '--debug'
    ])
    assert "非法路径。仅单个文件路径是合法的" in result.output


def test_svn_import_with_invalid_file(tmpdir):
    # 上传文件不存在
    runner = CliRunner()
    result = runner.invoke(app, [
        '--username', 'huangxiaojun', '--password', 'huangxiaojun', '--url',
        'svn://localhost/proj1/trunk', '--path', tmpdir, '--filename',
        'dir1.txt', '--debug'
    ])
    assert result.output == f"{tmpdir}/dir1.txt不存在。\n"
