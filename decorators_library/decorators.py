import signal
import os
import logging

from collections import Hashable, defaultdict
from functools import wraps
from .exceptions import FunctionTimeoutException


def inspect(func):
    """
    Decorator. Prints a function's arguments and return value when called.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        s = str(args)[1:-1]
        if kwargs:
            for key, value in kwargs.items():
                s += ", {}={}".format(key, value)

        print("{} invoked with {}. Result: {}".format(func.__name__, s, func(*args, **kwargs)))
        return func(*args, **kwargs)

    return wrapper


def timeout(seconds, exception=FunctionTimeoutException):
    """
    Decorator.  Throws an exception if given number of seconds elapse while the function
    is still executing.
    """

    def func_wrapper(func):
        def receive_alarm(signum, stack):
            raise exception('Function call timed out')

        @wraps(func)
        def inner(*args, **kwargs):
            if os.name is "posix":
                signal.signal(signal.SIGALRM, receive_alarm)
                signal.alarm(seconds)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
                return result
            else:
                return func(*args, **kwargs)

        return inner

    return func_wrapper


def memoized(func):
    """
    Decorator. Caches a function's return value each time it is called.
    If the function has already been called with given arguments the cached
    value is returned instead.
    """
    cache = func.cache = {}

    @wraps(func)
    def inner(*args):
        if isinstance(args, Hashable):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        else:
            return func(*args)

    return inner


def count_calls(func):
    """
    Decorator.  Tracks the number of times that each decorated function is called.
    """
    if not hasattr(count_calls, '__counters'):
        count_calls.__counters = defaultdict(int)

    count_calls.counters = lambda: count_calls.__counters
    func.counter = lambda: count_calls.__counters[func.__name__]

    count_calls.reset_counters = lambda: count_calls.__counters.clear()

    @wraps(func)
    def inner(*args, **kwargs):
        count_calls.__counters[func.__name__] += 1
        return func(*args, **kwargs)

    return inner


# class debug(object):
#     """
#     Decorator.  Logs a message before starting the execution including given params, and a
#     second message after the execution is finished with the returned result
#     TODO: Finish this
#     """
#
#     def __init__(self, func, logger=None):
#         self.func = func
#         self.logger = logger
#
#     def __call__(self, *args, **kwargs):
#         if not self.logger:
#             logging.basicConfig(level=logging.DEBUG)
#             self.logger = logging.getLogger(self.func.__module__)
#
#         @wraps(self.func)
#         def wrapper():
#             self.logger.debug('Executing "{}" with params: {}, {}'.format(self.func.__name__, args, kwargs))
#             res = self.func(*args, **kwargs)
#             self.logger.debug('Finished "{}" execution with result: {}'.format(self.func.__name__, res))
#             return res
#
#         return wrapper()


def debug(logger=None):
    """
    Decorator.  Logs the decorated function and arguments to the debug stream before and after execution.
    Optionally receives a custom logger.
    """

    def wrapper(func):
        nonlocal logger
        if not logger:
            logger = logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(func.__module__)

        @wraps(func)
        def inner(*args, **kwargs):
            logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
            res = func(*args, **kwargs)
            logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, res))
            return res

        return inner

    return wrapper
