import signal
import logging
from functools import wraps
from .exceptions import FunctionTimeoutException

# implement your decorators here.


def inspect(fn):
    def new_add(*args, **kwargs):
        result = fn(*args, **kwargs)
        if not kwargs or kwargs['operation'] == 'add':
            extra_text = ''
        else:
            extra_text = ', operation={}'.format(kwargs['operation'])
        print('{} invoked with {}, {}{}. Result: {}'.format(fn.__name__, args[0], args[1], extra_text, result))
        return result
    return new_add


class timeout(object):

    def __init__(self, timeout, exception=FunctionTimeoutException):
        self.timeout = timeout
        self.exception = exception

    def receive_alarm(self, signum, stack):
        raise self.exception('Function call timed out')

    def __call__(self, fn):
        def new_fn(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.receive_alarm)
            signal.alarm(self.timeout)
            result = fn(*args, **kwargs)
            signal.alarm(0)
            return result
        return new_fn


class memoized(object):

    def __init__(self, fn):
        self.cache = {}
        self.fn = fn

    def __call__(self, *args):
        if not self.cache.get(args):
            result = self.fn(*args)
            self.cache[(args)] = result
            return result
        else:
            return self.cache.get(args)


class count_calls(object):

    glob_count = {}

    def __init__(self, fn):
        self.ind_count = 0
        self.fn = fn
        if not type(self).glob_count.get(self.fn.__name__):
            type(self).glob_count[self.fn.__name__] = 0

    def __call__(self):
        type(self).glob_count[self.fn.__name__] += 1
        self.ind_count += 1
        return self.fn()

    def counter(self):
        return self.ind_count

    @classmethod
    def counters(cls):
        return cls.glob_count

    @classmethod
    def reset_counters(cls):
        cls.glob_count = {}


def debug(**kwargs):
    def decorator(fn):
        @wraps(fn)
        def decorated(*args):
            if not kwargs.get('logger'):
                logger = logging.getLogger(fn.__module__)
            else:
                logger = kwargs.get('logger')
            logger.debug('Executing "{}" with params: {}, {}'.format(fn.__name__, args, kwargs))
            result = fn(*args)
            logger.debug('Finished "{}" execution with result: {}'.format(fn.__name__, str(result)))
            return result
        return decorated
    return decorator
