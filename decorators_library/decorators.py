import signal
from .exceptions import TimeoutError
from functools import wraps
import logging

# implement your decorators here.
class count_calls(object):
    cls_counter = {}
    
    def __init__(self, func):
        self.func = func
        self.count = 0
        count_calls.cls_counter[func.__name__] = 0
        

    def __call__(self, *args, **kwargs):
        self.count += 1
        count_calls.cls_counter[self.func.__name__] = self.count
        return self.func(*args, **kwargs)
        
    def counter(self):
        return self.count
        
    @classmethod
    def counters(cls):
        return cls.cls_counter
        
    @classmethod
    def reset_counters(cls):
        cls.cls_counter.clear()

class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
            
    
def timeout(seconds = 10):
    "Simpel decorator to stop after certain time"
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper 
    return decorator


def signal_handler(signum, frame):
    raise TimeoutError("Function call timed out.")
    
def debug(logger=None):
    log = logger
    def real_dec(function):
        if not log:
            logger = logging.getLogger(function.__module__)
        else:
            logger=log
        def wrapper(*args, **kwargs):
            return_val = function(*args, **kwargs)
            logger.debug('Executing "{}" with params: {}, {{}}'.format(function.__name__,\
            tuple(args)))
            logger.debug('Finished "{}" execution with result: {}'.format(function.__name__,\
            return_val))
            return return_val
        return wrapper
    return real_dec