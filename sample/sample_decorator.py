
def log_record(view_func):
    def __wrapper(*args, **kwargs):
        print("log record")
        return view_func(*args, **kwargs)
    return __wrapper


@log_record
def test():
    b = 1 + 2
    print(b)


if __name__ == "__main__":
    test()