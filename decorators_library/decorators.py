# implement your decorators here.
import time
import functools
import logging
import signal #for timeout decorator

from .exceptions import TimeoutError

# @memoized decorator
class memoized(object):
    
    def __init__(self, func):
        self.cache = {}
        self.func = func
        
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            result = self.func(*args)
            self.cache[args] = result
            return result


# @count_calls decorator
class count_calls(object):
    countDict = {}
    
    def __init__(self, func):
        self.func = func
        count_calls.countDict[func.__name__] = 0
        
    def __call__(self, *args, **kwargs):
        count_calls.countDict[self.func.__name__] += 1
        return self.func(*args, **kwargs)
        
    def counter(self):
        return count_calls.countDict[self.func.__name__]
        
    @classmethod
    def counters(cls):
        return cls.countDict
        
    @classmethod
    def reset_counters(cls):
        cls.countDict.clear()

# timeout decorator
class timeout(object):
    def __init__(self, threshold=1):
        self.threshold = threshold

    def __call__(self, fn):
        def wrapper(*args, **kwds):
            t0 = time.time()
            fn(*args, **kwds)
            t1 = time.time()
            exec_time = t1 - t0
            if exec_time >= self.threshold:
                raise TimeoutError('Function call timed out')
            return fn(*args, **kwds)
            
        return wrapper
    
# debug decorator

class debug(object):
    
    def __init__(self, logger=None):
        self.logger = logger
        
    def __call__(self, f):
        if not self.logger:
            self.logger = logging.getLogger(f.__module__)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(f.__name__, args, kwargs))
            result = f(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(f.__name__, result))
            return f(*args, **kwargs)
        return wrapper
