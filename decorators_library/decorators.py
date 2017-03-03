import time
import signal
import logging
from .exceptions import TimeoutError


class debug(object):
    def __init__(self, logger=None):
        self.logger = logger   
        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            my_func = func(*args, **kwargs)
            
            if not self.logger:
                self.logger = logging.getLogger(func.__module__)
                self.logger.setLevel(logging.DEBUG)
            self.logger.debug('Executing "%s" with params: %s, %s', func.__name__, args, kwargs)
            self.logger.debug('Finished "%s" execution with result: %s', func.__name__, my_func)
            return my_func
        return wrapper
        
        
class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        my_func = self.func(*args)
        if (args[0],args[1]) not in self.cache:
            self.cache[(args[0],args[1])] = my_func
            return my_func
        else:
            return self.cache[(args[0],args[1])]
  
        
class count_calls(object):
    cache_count = {}
    def __init__(self, func):
        self.func = func
        
    def __call__(self):
        if self.func.__name__ not in count_calls.cache_count.keys():
            count_calls.cache_count[self.func.__name__] = 0
        count_calls.cache_count[self.func.__name__] += 1
        return self.func
    
    def counter(self):
        if self.func.__name__ in count_calls.cache_count.keys():
            return count_calls.cache_count[self.func.__name__]
        else:
            count_calls.cache_count[self.func.__name__] = 0 
            return count_calls.cache_count[self.func.__name__]
    @classmethod    
    def counters(self):
        return count_calls.cache_count
    
    @classmethod 
    def reset_counters(self):
        count_calls.cache_count = {}
        
        
class timeout(object):
    
    def __init__(self, allowed_time):
        
        self.allowed_time = allowed_time
        
    def _handle_timeout(self, signum, frame):
        raise TimeoutError("Function call timed out") 
        
    def __call__(self, func):
        def wrapped():
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self.allowed_time)
            try:
                result = func()
            finally:
                signal.alarm(0)
            return result
        return wrapped





            