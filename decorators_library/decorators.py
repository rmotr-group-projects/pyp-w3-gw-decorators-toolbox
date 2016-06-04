import time
from .exceptions import TimeoutError
from logging import getLogger


class Timeout(object):
    def __init__(self, func, max_time):
        self.func = func
        self.max_time = max_time
    
    def __call__(self, *args, **kwargs):
        start = time.time()
        return_val = self.func(*args, **kwargs)
        end = time.time()
        
        if end - start > self.max_time:
            raise TimeoutError('Function call timed out')
        return return_val

def timeout(max_time):
    def decorator(func):
        return Timeout(func, max_time)
    return decorator

def debug(logger=None):
    def other(func):
        def wrapper(*args, **kwargs):
            return_val = func(*args, **kwargs)
            if logger is not None:
                log = logger
            else:  
                log = getLogger('tests.test_decorators')
                log.debug('Executing "{}" with params: {}, {{}}'.format(func.__name__, tuple(args)))
                
                log.debug('Finished "{}" execution with result: {}'.format(func.__name__, return_val))
            return return_val
        return wrapper
    return other
  
class count_calls(object):
    
    func_calls = {}
    
    def __init__(self,func):
        self.func_name = func.__name__
        self.func_calls.setdefault(self.func_name, 0)
        

    def counter(self):
        return self.func_calls[self.func_name]
        
    @classmethod
    def counters(self):
        return self.func_calls
        
    @classmethod
    def reset_counters(self):
        self.func_calls = {}
    
    def __call__(self):
        self.func_calls[self.func_name] += 1
    
    
class memoized:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args, **kwargs):
        return_val = self.func(*args, **kwargs)
        call_dict = {tuple(args) : return_val}
        self.cache.update(call_dict)
        return return_val
        
    