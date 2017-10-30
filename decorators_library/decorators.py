import signal
import logging
from .exceptions import *


def inspect(fn):

    def new_fn(*args, **kwargs):
        arg_list = []
        result = fn(*args, **kwargs)
        for arg in args:
            arg_list.append(str(arg))
        for kwarg in kwargs:
            arg_list.append(str(kwarg)+'='+kwargs[kwarg])
        print ('{} invoked with {}. Result: {}'.
               format(fn.__name__, ', '.join(arg_list), result))
        return result
    return new_fn


class count_calls(object):
    counter_cache = {}

    def __init__(self, fn):
        self.fn = fn
        count_calls.counter_cache[self.fn.__name__] = 0
        self.count = count_calls.counter_cache[self.fn.__name__]

    def __call__(self):
        count_calls.counter_cache[self.fn.__name__] += 1

    def counter(self):
        return count_calls.counter_cache[self.fn.__name__]

    @classmethod
    def reset_counters(cls):
        cls.counter_cache.clear()

    @classmethod
    def counters(cls):
        return cls.counter_cache


class timeout(object):

    def __init__(self, max_time, exception=FunctionTimeoutException):
        self.max_time = max_time
        self.exception = exception

    def call_exception(self, signum, stack):
        raise self.exception('Function call timed out')

    def __call__(self, fn):
        def new_fn(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.call_exception)
            signal.alarm(self.max_time)
            result = fn(*args, **kwargs)
            signal.alarm(0)
            return result
        return new_fn


class memoized(object):

    def __init__(self, fn):
        self.fn = fn
        self.cache = {}

    def __call__(self, *args, **kwargs):
        def cach_check(*args, **kwargs):
            try:
                return self.cache[args]
            except KeyError:
                self.cache[args] = self.fn(*args, **kwargs)
                return self.cache[args]
        return cach_check(*args, **kwargs)


class debug(object):

    def __init__(self, logger= None):
        if not logger:
            logging.basicConfig()
            self.logger = logging.getLogger('tests.test_decorators')
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger = logger

    def __call__(self, fn):
        def new_fn(*args, **kwargs):
            self.logger.log(10,'Executing "%s" with params: %s, %s',fn.__name__, args, kwargs)
            result = fn(*args, **kwargs)
            self.logger.log(10,'Finished "{}" execution with result: {}'.format(
                   fn.__name__,result))
            return result
        return new_fn
