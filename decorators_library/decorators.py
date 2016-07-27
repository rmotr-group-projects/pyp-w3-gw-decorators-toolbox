import signal
import logging
from .exceptions import TimeoutError
from functools import wraps

class count_calls(object):
    
    keep_all_counts = {}
    
    def __init__(self, fn):
        self.fn = fn
        count_calls.keep_all_counts[fn.__name__] = 0
    
    def __call__(self):
        count_calls.keep_all_counts[self.fn.__name__] += 1
        
        def nested_func():
            return self.fn()
        return nested_func
    
    def counter(self):
        return count_calls.keep_all_counts[self.fn.__name__]
    
    @classmethod
    def counters(cls):
        return count_calls.keep_all_counts
    
    @classmethod
    def reset_counters(cls):
        count_calls.keep_all_counts = {}


class debug(object):
    
    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, f):
        #@wraps
        def nested_func(*args, **kwargs):  #def function(unnamedarg1, unnamedarg2, namedarg1=1, namedarg2='two') args = (1, 2) kwargs = {namedarg:1, namedarg2='two'}
            ex = 'Executing "{}" with params: {}, {}'.format(f.__name__, args, kwargs)
            if not self.logger:
                self.logger = logging.getLogger(f.__module__)
            
            result = f(*args, **kwargs)
            end = 'Finished "{}" execution with result: {}'.format(f.__name__, str(result))
            
            # load messages to log
            self.logger.debug(ex)
            self.logger.debug(end)
            
            
            return result
        return nested_func


class memoized(object):
    
    def __init__(self,original_function):
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