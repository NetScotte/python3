# -*- coding=utf-8 -*-
import pathlib


def escape_semicolon(file, encoding='utf-8'):
    """将file文件中的分号替换成'||';'||'

    :param file: 文件路径
    :type file: str
    :param encoding: 文件编码, defaults to 'utf-8'
    :param encoding: str, optional
    :raises FileNotFoundError: 文件不存在
    :return: 替换后的文件字符串
    :rtype: str
    """

    if not pathlib.Path(file).exists():
        raise FileNotFoundError(f'{file}不存在')
    replaced_file_str = ''
    with open(file, 'r', encoding=encoding) as f:
        flag = False
        for line in f:
            for c in line:
                if c == "'":
                    flag = not flag
                if flag and c == ';':
                    c = "'||';'||'"
                replaced_file_str += c
    return replaced_file_str


if __name__ == '__main__':
    import os
    s = """
asjdifpa
'asdfasdf;asdfasd'
asdf;
'asdf;
'
"""
    with open('testfile.sql', 'w') as f:
        f.write(s)
    print(escape_semicolon('atestfile.sql'))
    os.remove('testfile.sql')
