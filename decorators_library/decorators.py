from functools import wraps
import signal
from decorators_library.exceptions import *
import logging
        

def memoized(func):
    @wraps(func)
    def memfunc(*args):
        if args not in memfunc.cache:
            memfunc.cache[args] = func(*args)
        return memfunc.cache[args]
    memfunc.cache = {}
    return memfunc


class count_calls(object):
    _counters = {}
    
    def __init__(self, func):
        self._counters[func.__name__] = 0
        self.func = func
        
        
    def __call__(self, *args, **kwargs):
        self._counters[self.func.__name__] += 1
        return self.func(*args, **kwargs)
            
        
    def counter(self):
        return self._counters[self.func.__name__]

    @classmethod
    def counters(cls):
        return cls._counters
        
    @classmethod
    def reset_counters(cls):
        cls._counters.clear()


#warning: don't trust this for functions with recursive calls
def timeout(limit, func = None):
    if func is None:
        return lambda func: timeout(limit, func)
    def alarm(signum, frame):
        raise TimeoutError('Function call timed out')
    @wraps(func)
    def timefun(*args, **kwargs):
        signal.signal(signal.SIGALRM, alarm) 
        signal.alarm(limit)
        res = func(*args, **kwargs)
        signal.alarm(0)
        return res
    return timefun
    
class debug(object):
    
    def __init__(self, logger = None):
        self.logger = logger
    
    def __call__(self, func):
        if self.logger is None:
            self.logger = logging.getLogger(func.__module__)
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.debug('Executing "{}" with params: {}, {}'.format(func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(func.__name__, result))
            return result
        return wrapper
        
def count_doc(func):
    orig_doc = func.__doc__
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        wrapper.__doc__ = orig_doc + '\n\n{} has been called {} times.'.format(func.__name__, wrapper.count)
        return func(*args, **kwargs)
    wrapper.__doc__ = orig_doc + '\n\n{} has never been called.'.format(func.__name__)
    wrapper.count = 0
    return wrapper