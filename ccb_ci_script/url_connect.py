# -*- coding=utf-8 -*-
import click
import requests
import time

from log import logger
from cmd_context import pass_context
from common import log_pid
from exceptions import ExceptionsParse
from requests.exceptions import RequestException, ConnectionError, HTTPError


@click.command()
@click.option('--url', required=True, help='验证url地址')
@click.option('--time_out', help='超时时间')
@click.option('--taskid')
@click.option('--verbose', '-v', is_flag=True, help='输出详细内容')
@click.option('--debug', is_flag=True, help='debug模式')
@pass_context
def main(ctx, taskid, verbose, debug, url, time_out):
    if debug:
        logger.debug_on()
    log_pid(taskid)
    ctx.verbose = verbose
    run_time = 0

    # 请求url，获取页面返回值
    while run_time <= float(time_out):

        try:
            r = requests.get(url).status_code
        # 错误信息不做处理
        except RequestException:
            ReferenceError
        except RequestException:
            HTTPError
        except RequestException:
            ConnectionError
        except Exception as e:
            ExceptionsParse(e)
        else:
            # 页面返回值为200或300为页面访问正常
            if 200 <= r <= 399:
                break
        # 返回值不为200休眠3秒，重新请求
        time.sleep(3)
        run_time = time.perf_counter()

    else:
        click.echo('页面访问异常，请尽快人工干预查看服务状态')
        exit(1)
    click.echo('页面访问正常')
    exit(0)


if __name__ == '__main__':
    main()
