import signal
import os
import logging
import inspect as std_inspect

from collections import Hashable, defaultdict
from functools import wraps
from decorators_library.exceptions import FunctionTimeoutException


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


class debug(object):
    """
    Decorator.  Logs a message before starting the execution including given params, and a
    second message after the execution is finished with the returned result
    """

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        if not self.logger:
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(func.__module__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
            res = func(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, res))
            return res

        return wrapper


# Function based implementation of the debug decorator
#
# def debug(logger=None):
#     """
#     Decorator.  Logs the decorated function and arguments to the debug stream before and after execution.
#     Optionally receives a custom logger.
#     """
#     debug.logger = logger
#
#     def wrapper(func):
#         logger = debug.logger
#         if not logger:
#             logger = logging.basicConfig(level=logging.DEBUG)
#             logger = logging.getLogger(func.__module__)
#
#         @wraps(func)
#         def inner(*args, **kwargs):
#             logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
#             res = func(*args, **kwargs)
#             logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, res))
#             return res
#
#         return inner
#
#     return wrapper


def add_method(cls, instance_method=True):
    """
    Decorator.  Adds the decorated function to the passed in class, will insert self
    param if missing and the method is to be an instance method.
    """

    def wrapper(method):
        method_params = std_inspect.getargspec(method).args

        if instance_method and 'self' not in method_params:
            @wraps(method)
            def new_method(self, *args, **kwargs):
                return method(*args, **kwargs)

            setattr(cls, method.__name__, new_method)
        elif instance_method:
            setattr(cls, method.__name__, method)
        else:
            @staticmethod
            def new_method(*args, **kwargs):
                return method(*args, **kwargs)

            setattr(cls, method.__name__, new_method)
        return cls

    return wrapper


def singleton(cls):
    """
    Decorator.  Returns an already created instance of the decorated class if one exists
    """
    instances = dict()

    @wraps(cls)
    def check_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return instances[cls]

    return check_instance
