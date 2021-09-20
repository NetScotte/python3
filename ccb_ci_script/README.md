# Shepherd脚本 README

## 如何查看文档

``` bash
    > pip install -r requirements-doc.txt
    > cd docs
    > make html
```

文档将会生成在 ``docs/build/html`` 中，首页 **index.html**

## 公共模块

### _template.py

脚本模版

### common.py

isolated_filesystem

    用于建立一个临时文件夹的隔离区域

b2s

    将bytes字符串根据当前系统的编码转成utf-8字符串

log_pid

    配合kill_pid.py脚本用来处理进程杀死功能

### cmd_context.py

    脚本上下文管理，主要内容是verbose、err输出

### exceptions.py

    用来分析错误原始信息，将其转换成可读性信息

### log.py

    日志输出控制
