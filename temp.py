from threading import Thread
from functools import wraps
from time import sleep


def myasync(func):
    @wraps(func)
    def async_func(*args, **kwargs):
        # func_hl = Process(target = func, args = args, kwargs = kwargs)
        func_hl = Thread(target = func, args = args, kwargs = kwargs)
        func_hl.start()
        return func_hl

    return async_func


@myasync
def print_somedata():
    print('starting print_somedata')
    sleep(2)
    print('print_somedata: 2 sec passed')
    sleep(2)
    print('print_somedata: 2 sec passed')
    sleep(2)
    print('finished print_somedata')


def main():
    print_somedata()
    print('back in main')
    print_somedata()
    print('back in main')


if __name__ == '__main__':

    main()