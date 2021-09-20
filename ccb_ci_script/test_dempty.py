# -*- coding=utf-8 -*-
from click.testing import CliRunner
from dempty import main as app


def test_dempty_with_empty_directory(tmpdir):
    path = str(tmpdir)
    runner = CliRunner()
    result = runner.invoke(app, [path])
    assert result.exit_code == 1
    assert result.output == '程序文件夹为空，不需要进行打包任务。\n'


def test_dempty_with_noempty_directory(tmpdir):
    t = tmpdir.join("test_file.txt")
    t.write("This is test file.")
    path = str(tmpdir)
    runner = CliRunner()
    result = runner.invoke(app, [path])
    assert result.exit_code == 0
    assert result.output == '本次程序文件有变更，需要进行打包任务。\n'
