import signal
import logging
from .exceptions import TimeoutError
from functools import wraps

class count_calls(object):
    keep_all_counts = {}
    
    def __init__(self, fn):
        self.fn = fn
        self.keep_all_counts[self.fn.__name__] = 0
    
    def __call__(self):
        self.keep_all_counts[self.fn.__name__] += 1
        return self.fn
    
    def counter(self):
        return self.keep_all_counts[self.fn.__name__]
    
    @classmethod
    def counters(cls):
        return cls.keep_all_counts
    
    @classmethod
    def reset_counters(cls):
        cls.keep_all_counts = {}


class debug(object):
    
    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, fn):
        
        def debugging(*args, **kwargs):
            if not self.logger:
                self.logger = logging.getLogger(fn.__module__)
            
            name = fn.__name__
            ex = 'Executing "{}" with params: {}, {}'.format(name, args, kwargs)
            result = fn(*args, **kwargs)
            end = 'Finished "{}" execution with result: {}'.format(name, result)
            
            self.logger.debug(ex)
            self.logger.debug(end)
            return result

        return debugging


class memoized(object):
    def __init__(self, original_function):
        self.original_function = original_function
        self.cache = {}
    
    def __call__(self,*args,**kwargs):
        if args in self.cache:
            return self.cache[args]
        self.cache[args] = self.original_function(*args,**kwargs)
        return self.original_function(*args,**kwargs)
            
            
def signal_handler(signalnum, frame):
    raise TimeoutError('Function call timed out')


def timeout(timeout_seconds=0):
    """
    Decorator that allows user to specify a length of time in seconds to timeout
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(timeout_seconds)
            try:
                return func(*args, **kwargs)
            except:
                raise TimeoutError('Function call timed out')
            finally:
                signal.alarm(0)
        return wrapper
    return decorate