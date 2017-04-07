# implement your decorators here.
import signal
import time
import functools
import logging

from decorators_library.exceptions import TimeoutError

#@timeout
def timeout(sec):
    def decorator_function(fn):
        def _handle_timeout(signum, frame):
            raise TimeoutError("Function call timed out")
        
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(sec)
            try:
                result = fn(*args,**kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator_function

#@debug()
def debug(logger=None):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if not logger:
                _logger = logging.getLogger(fn.__module__)
            else:
                _logger = logger
            
            _logger.debug('Executing "{}" with params: {}, {}'.format(fn.__name__,args, kwargs))
            result = fn(*args,**kwargs)
            _logger.debug('Finished "{}" execution with result: {}'.format(fn.__name__, result))
            return result
        return wrapper
    return decorator

#@count_calls
class count_calls(object):
    
    counters_log = {}
    
    def __init__(self,fn):
        self.count = 0
        self.fn = fn
        count_calls.counters_log[self.fn.__name__] = 0
        
    def __call__(self):
        self.count += 1
        count_calls.counters_log[self.fn.__name__] += 1
        return self.fn
        
    
    def counter(self):
        return self.count
    
    @classmethod
    def counters(cls):
        return cls.counters_log
    
    @classmethod
    def reset_counters(cls):
        cls.counters_log = {}

#@memoized
class memoized(object):
    
    def __init__(self,fn):
        self.cache = {}
        self.fn = fn
        
    def __call__(self,*args):
        self.cache[args] = self.fn(*args)
        return self.fn(*args)