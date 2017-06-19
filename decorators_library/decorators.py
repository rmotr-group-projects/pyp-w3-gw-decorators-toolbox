from __future__ import print_function
from functools import wraps
from collections import defaultdict

import logging
import time
import signal

try:
    from decorators_library.exceptions import *
except ImportError:
    from exceptions import *

class timeout(object):
    def __init__(self, length=5):
        self.length = length

    def __call__(self, function):
        def _handle_timeout(signum, frame):
            raise TimeoutError('Function call timed out')

        @wraps(function)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(self.length)

            try:
                result = function(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

class debug(object):
    
    def __init__(self, logger=None):
        self.logger = logger
    
    def __call__(self, function):
        if not self.logger:
            self.logger = logging.getLogger(function.__module__)
            
        @wraps(function) 
        def wrapper(*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(function.__name__, args, kwargs))
            self.logger.debug('Finished "{}" execution with result: {}'.format(function.__name__, function(*args)))

            return function(*args, **kwargs)
        return wrapper
    
class count_calls(object):
    class_counts = {}

    def __init__(self, function):
        self.counts = defaultdict(int)
        self.function = function

    def __call__(self):
        self.counts[self.function.__name__] += 1
        self.update_class_count(self.counts)

    def counter(self):
        if self.function.__name__ not in self.counts:
            self.counts[self.function.__name__] = 0
            self.update_class_count(self.counts)
            return 0
        return self.counts[self.function.__name__]

    @classmethod
    def reset_counters(cls):
        cls.class_counts = {}

    @classmethod
    def update_class_count(cls, updated_count):
        cls.class_counts.update(updated_count)

    @classmethod
    def counters(cls):
        return cls.class_counts


class memoized(object):
    def __init__(self, function):
        self.operations = defaultdict(dict)
        self.function = function
        self.cache = self.operations[self.function.__name__]

    def __call__(self, *args):
        operation = {args: self.function(*args)}
        if operation[args] not in self.operations[self.function.__name__].values():
            self.operations[self.function.__name__].update(operation)
            return self.function(*args)
        else:
            return self.operations[self.function.__name__][args]

