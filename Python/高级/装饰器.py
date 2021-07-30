#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import wraps


# 函数装饰器
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


# 带参数的函数装饰器
def my_decorator_num(num):
    def total(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(num)
            return func(*args, **kwargs)

        return wrapper

    return total


# 类装饰器
class Wraps(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


@my_decorator_num(1)
def run():
    print(11)


if __name__ == '__main__':
    run()
