import signal
import logging
import functools
import collections

from decorators_library.exceptions import *


def timeout(seconds, error_message='Function call timed out'):
    # HINT: check the `alarm` function in `signal` module
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorated


class debug(object):
    PRE_EXECUTION_MSG = 'Executing "{}" with params: {}, {}'
    POST_EXECUTION_MSG = 'Finished "{}" execution with result: {}'

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        # if a custom logger was not given, configure a default one
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.debug(
                self.PRE_EXECUTION_MSG.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            self.logger.debug(
                self.POST_EXECUTION_MSG.format(func.__name__, result))
            return result
        return wrapper



class count_calls(object):
    FUNCTION_COUNTERS = {}

    def __init__(self, func):
        self.func = func
        self.num_of_calls = 0
        count_calls.FUNCTION_COUNTERS[func] = self

    def __call__(self, *args, **kwargs):
        self.num_of_calls += 1
        return self.func(*args, **kwargs)

    def counter(self):
        return count_calls.FUNCTION_COUNTERS[self.func].num_of_calls

    @classmethod
    def counters(cls):
        return dict([(f.__name__, cls.FUNCTION_COUNTERS[f].num_of_calls)
                     for f in cls.FUNCTION_COUNTERS])

    @classmethod
    def reset_counters(cls):
        cls.FUNCTION_COUNTERS = {}


class memoized(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
